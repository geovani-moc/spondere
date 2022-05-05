from typing import Dict, List
from fastapi import (
    APIRouter, 
    Depends,
    File,
    UploadFile,
    Request, 
    BackgroundTasks, 
    HTTPException)
from controller.security import (
    JWTBearer,
    getCurrentUserName,
    getCurrentUserType)
from entity.biometrics import Biometrics
from entity.frequency import Frequency
from util.image import checkUploadedImage, imagesInFolder
from recognition.findFace import findFace
from recognition.faceRecognition import verifyFace
from database import biometrics as biometryDB
from database import frequency as frequencyDB
from database import academicClass as academicClassDB
from database import groupStudent as groupStudentDB
from database import user as userDB
from datetime import datetime
from util.image import imageContainsFace
from util.files import createUserImagesPath, removeAllFilesInFolder
from settings import(
    USER_TYPE_ADMIN,
    USER_TYPE_PROFESSOR,
    USER_TYPE_STUDENT,
    PATH_IMAGES,
    TIMEZONE_API_SERVER,
    MAX_SIZE_DATASET
)
from pathlib import Path
import aiofiles
import time
from util.recognition import(
    deleteTrain,
    readAllLabels,
    readAllTrains,
    updateTrain
)
import time

router = APIRouter()

@router.post("/checar/", dependencies=[Depends(JWTBearer())])
async def checkBiometry(request:Request, studentID:int, classID:int, ble:bool,
    qrcode:bool, validationCode:str, latitude:float, longitude:float,
    backgroundTasks:BackgroundTasks, file: UploadFile = File(...))->Dict:

    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)
    username = getCurrentUserName(authorization)

    if userType != USER_TYPE_STUDENT:
        raise HTTPException(status_code=401,
            detail="Somente alunos podem checar biomátria.")

    if not isCheckable(username, classID):
        raise HTTPException(status_code=406,
            detail="b001")
    try:
        if frequencyDB.existValid(studentID, classID):
            return {"result": "Já existe uma presença válida."}
    except:
        raise HTTPException(status_code=406,
            detail="f002")

    contents = await file.read()

    frequency = Frequency()
    frequency.ManualAttendance = False
    frequency.academicClassID = classID
    frequency.studentID = studentID
    frequency.BLEAttendance = ble
    frequency.QrCodeAttendance = qrcode
    frequency.validationCode = validationCode
    frequency.latitude = latitude
    frequency.longitude = longitude

    backgroundTasks.add_task(processBiometrics, frequency, studentID, contents)

    return {"result": "Imagem recebida, em processamento."}

def processBiometrics(frequency:Frequency, userID:int, contents):
    start = time.time()
    image = checkUploadedImage(contents)
    
    if image is None:
        frequency.failure = "Falha na imagem recebida."
        try:
            id = frequencyDB.create(frequency=frequency)
        except Exception as e:
            print(type(e))   
            print(e.args)
        return

    face, error = findFace(image)
    if error:
        frequency.failure = "Falha no reconhecimento facial."
        print("Erro no sistema de reconhecimento facial: \n" + error)
        try:
            id = frequencyDB.create(frequency=frequency)
        except Exception as e:
            print(type(e))   
            print(e.args)
        return
            
    result, error = verifyFace(face, userID)
    if not result: 
        frequency.failure = error
    else:
        frequency.photo = contents
        
    try:
         id = frequencyDB.create(frequency)
    except Exception as e:
        print(type(e))   
        print(e.args)
        return
    end = time.time()
    print(f'A frequencia com id:{id} foi criada. Tempo para verificação biometrica:{end-start}')

@router.post("/{studentID}", dependencies=[Depends(JWTBearer())])
async def createBiometry(backgroundTasks:BackgroundTasks, request:Request, 
    studentID:int, files:List[UploadFile] = File(...)) -> dict:

    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if userType != USER_TYPE_ADMIN and studentID != user.id:
        raise HTTPException(status_code=401,
            detail="O usuário não tem privilegio de administrador ou não é o usuário proprietário.")

    if biometryDB.existValidBiometry(studentID):
        raise HTTPException(status_code=401,
            detail="O usuário já tem uma biometria válida.")

    userImagesPath:str = PATH_IMAGES + '/' + f'{studentID}'
    Path(userImagesPath).mkdir(parents=True, exist_ok=True)

    for file in files:
        if(imagesInFolder(userImagesPath) > MAX_SIZE_DATASET):
            break
        content = await file.read()
        if imageContainsFace(content):
            path = userImagesPath + '/' + f'{time.time()}' + "_" + file.filename
            async with aiofiles.open(path, 'wb') as outFile:
                await outFile.write(content)

    biometry = Biometrics()
    biometry.studentID = studentID
    biometry.active = True
    biometry.invalid = True
    biometry.failure = None
    id = biometryDB.create(biometry)
    backgroundTasks.add_task(syncTrain, studentID, id)
    return {
        "id": id
    }

@router.put("/adicionar_fotos/{biometryID}", dependencies=[Depends(JWTBearer())])
async def updateBiometry(backgroundTasks:BackgroundTasks, biometryID:int, 
    request:Request, files:List[UploadFile] = File(...))-> dict:

    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)
    username = getCurrentUserName(authorization)
    user = userDB.read(username)
    biometry = biometryDB.read(biometryID)

    if userType != USER_TYPE_ADMIN and biometry.studentID != user.id:
        raise HTTPException(status_code=401,
            detail="O usuário não tem privilegio de administrador ou não é o usuário proprietário.")

    if not biometry.active:
        raise HTTPException(status_code=403,
            detail="O usuário só pode adicionar fotos em uma biometria ativa.")

    userImagesPath:str = PATH_IMAGES + '/' + f'{biometry.studentID}'
    Path(userImagesPath).mkdir(parents=True, exist_ok=True)

    for file in files:
        if(imagesInFolder(userImagesPath) > MAX_SIZE_DATASET):
            break
        content = await file.read()
        if(imageContainsFace(content)):
            path = userImagesPath + '/' + f'{time.time()}' + "_" + file.filename
            async with aiofiles.open(path, 'wb') as outFile:
                await outFile.write(content)

    backgroundTasks.add_task(syncTrain, biometry.studentID, biometry.id)

    return{
        "result": "success"
    }

@router.put("/desabilitar/{biometryID}", dependencies=[Depends(JWTBearer())])
async def disableBiometry(biometryID:int, request:Request) -> Dict:
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")

    try:studentID = biometryDB.disable(biometryID)
    except:return{"result": "Error: b002"}

    path = createUserImagesPath(studentID)
    
    try: removeAllFilesInFolder(path)
    except: return {"result":"Error: b003"}

    return{"result": "success"}

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def getBiometry(id:int) -> dict:
    biometry = biometryDB.read(id)
    return {
        "biometry": biometry
    }

def syncTrain(userID:int, biometryID:int, methodName = 'cnn'):
    start = time.time()
    _, error = updateTrain(PATH_IMAGES, userID, methodName)
    readAllTrains(methodName)
    readAllLabels(methodName)

    if error is not None:
        if len(error) > 50:
            error = error[:50]
            print("conjunto de erro acumulado.[maior que o limite do banco de dados]")
        biometryDB.invalidate(biometryID, error)
        return

    biometryDB.validate(biometryID)
    end = time.time()
    print(f'Tempo para sicronizar treino (biometria ID: {biometryID})):{end-start}')

def isCheckable(username:str , classID:int)->bool:
    date = str(datetime.now())+str(TIMEZONE_API_SERVER)
    groupID, enddate = academicClassDB.infoCheckable(classID)
    if not groupStudentDB.exists(username, groupID):
        return False

    rightNow = datetime.fromisoformat(date)

    if rightNow > enddate:
        academicClassDB.blockAttendance(classID)
        return False

    return True

@router.get("/valida/{userID}", dependencies=[Depends(JWTBearer())])
async def isValidBiometry(userID:int) -> dict:
    result = 0
    try:
        result = biometryDB.isValid(userID)
    except:
        raise HTTPException(status_code=406,
            detail="Dados inválidos.")
    
    return result

@router.delete("/treinamento_completo", dependencies=[Depends(JWTBearer())])
async def deleteAllTrain(request:Request) -> dict:
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")
    
    try: deleteTrain("cnn")
    except: return{"result":"Error: b004"}
    
    return{"result":"success"}

@router.post("/refazer_treinamento_completo/", dependencies=[Depends(JWTBearer())])
async def redoTraining(backgroundTasks:BackgroundTasks, request:Request) -> Dict:
    methodName = 'cnn'
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")

    backgroundTasks.add_task(clearAndTrain, methodName)
        
    return{"result":"Processing request"}

def clearAndTrain(methodName):
    try:
        readAllTrains(methodName)
        readAllLabels(methodName)
    except: print(f'result:Error: b004')

@router.delete("/remover_dados_sensiveis/{username}", dependencies=[Depends(JWTBearer())])
async def removeAllSensitiveData(request:Request, username:str)->Dict:
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)
    errors = []

    if userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")
    
    try: 
        biometryID = biometryDB.readIDByUsername(username)
        studentID = biometryDB.disable(biometryID)
        path = createUserImagesPath(studentID)
        removeAllFilesInFolder(path)
        
    except: errors.append("Error: b003")

    try: frequencyDB.deleteAllFromUser(studentID)
    except: errors.append("não foi possivel apagar as frequências.")

    if len(errors) > 0: return {"result": errors}

    return{"result":"success"}