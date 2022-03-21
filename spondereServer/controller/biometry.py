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
    USER_TYPE_ADMIN,
    USER_TYPE_PROFESSOR,
    USER_TYPE_STUDENT,
    PATH_IMAGES
)
from pathlib import Path
import aiofiles
import time

router = APIRouter()

@router.post("/checar/", dependencies=[Depends(JWTBearer())])
async def checkBiometry(request:Request, studentID:int, classID:int, ble:bool,
    qrcode:bool, validationCode:str, latitude:float, longitude:float,
    backgroundTasks:BackgroundTasks, file: UploadFile = File(...))->Dict:
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
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

    backgroundTasks.add_task(processBiometrics, frequency, username, contents)

    return {"result": "Imagem recebida, em processamento."}

def processBiometrics(frequency:Frequency, username:str, contents):
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
            
    result, error = verifyFace(face, username)
    if not result: 
        frequency.failure = error
        
    try:
         id = frequencyDB.create(frequency)
    except Exception as inst:
        print(type(inst))   
        print(inst.args)
        return

    print("A frequencia com id: " + str(id) + " foi criada")


@router.post("{studentID}", dependencies=[Depends(JWTBearer())])
async def createBiometry(request:Request, studentID:int, files:List[UploadFile] = File(...)) -> dict:
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
        path = userImagesPath + '/' + f'{int(time.time())}' + "_" + file.filename
        async with aiofiles.open(path, 'wb') as outFile:
            while content := await file.read():  
                await outFile.write(content)

    biometry = Biometrics()
    biometry.studentID = studentID
    biometry.active = True
    biometry.invalid = False
    biometry.failure = None
    id = biometryDB.create(biometry)
    return {
        "id": id
    }

@router.put("/adcionar_fotos/{biometryID}", dependencies=[Depends(JWTBearer())])
async def updateBiometry(biometryID:int, request:Request, files:List[UploadFile] = File(...))-> dict:
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
        path = userImagesPath + '/' + f'{int(time.time())}' + "_" + file.filename
        async with aiofiles.open(path, 'wb') as outFile:
            while content := await file.read():  
                await outFile.write(content)

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
