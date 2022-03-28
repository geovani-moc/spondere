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
from util.image import checkUploadedImage
from recognition.findFace import findFace
from recognition.faceRecognition import verifyFace
from database import biometrics as biometryDB
from database import frequency as frequencyDB
from database import user as userDB
from util.files import createUserImagesPath, removeAllFilesInFolder
from settings import(
    LABELS,
    SVM_HOG,
    USER_TYPE_ADMIN,
    USER_TYPE_PROFESSOR,
    USER_TYPE_STUDENT,
    PATH_IMAGES
)
from pathlib import Path
import aiofiles
import time
from util.recognition import(
    readAllLabels,
    readAllTrains,
    train,
    updateTrain
)
from recognition.featureExtraction import extractFeature
#logger = logging.getLogger(__name__)


router = APIRouter()

@router.post("/checar/", dependencies=[Depends(JWTBearer())])
async def checkBiometry(studentID:int, classID:int, ble:bool,
    qrcode:bool, validationCode:str, latitude:float, longitude:float,
    backgroundTasks:BackgroundTasks, file: UploadFile = File(...))->Dict:
       
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
    image = checkUploadedImage(contents)
    
    if image is None:
        frequency.failure = "Falha na imagem recebida."
        try:
            id = frequencyDB.create(frequency=frequency)
        except Exception as inst:
            print(type(inst))   
            print(inst.args)
        return

    face, error = findFace(image)
    if error:
        frequency.failure = "Falha no reconhecimento facial."
        print("Erro no sistema de reconhecimento facial: \n" + error)
        try:
            id = frequencyDB.create(frequency=frequency)
        except Exception as inst:
            print(type(inst))   
            print(inst.args)
        return
            
    result, error = verifyFace(face, userID)
    if not result: 
        frequency.failure = error
    else:
        frequency.photo = contents
        
    try:
         id = frequencyDB.create(frequency)
    except Exception as inst:
        print(type(inst))   
        print(inst.args)
        return

    print("A frequencia com id: " + str(id) + " foi criada")


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
        path = userImagesPath + '/' + f'{time.time()}' + "_" + file.filename
        async with aiofiles.open(path, 'wb') as outFile:
            while content := await file.read():  
                await outFile.write(content)

    biometry = Biometrics()
    biometry.studentID = studentID
    biometry.active = True
    biometry.invalid = False
    biometry.failure = None
    id = biometryDB.create(biometry)
    backgroundTasks.add_task(syncTrain, studentID, id)
    return {
        "id": id
    }

@router.put("/adcionar_fotos/{biometryID}", dependencies=[Depends(JWTBearer())])
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
        path = userImagesPath + '/' + f'{time.time()}' + "_" + file.filename
        async with aiofiles.open(path, 'wb') as outFile:
            while content := await file.read():  
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

    studentID = biometryDB.disable(biometryID)
    path = createUserImagesPath(studentID)
    removeAllFilesInFolder(path)

    return{
        "result": "success"
    }


@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def getBiometry(id:int) -> dict:
    biometry = biometryDB.read(id)
    return {
        "biometry": biometry
    }

def syncTrain(userID:int, biometryID:int):
    methodName = 'hog'
    method = extractFeature

    _, error = updateTrain(PATH_IMAGES, userID, method, methodName)
    if error is not None:
        if len(error) > 50:
            error = error[:50]
            print("conjunto de erro acumulado.[maior que o limite do banco de dados]")
        biometryDB.invalidate(biometryID, error)
        return

    SVM_HOG, _ = readAllTrains(methodName, method)
    LABELS = readAllLabels(methodName)
    biometryDB.validate(biometryID)