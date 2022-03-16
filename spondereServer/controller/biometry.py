from typing import Dict
from fastapi import (
    APIRouter, 
    Depends,
    File, 
    Form,
    UploadFile,
    Request, 
    BackgroundTasks, 
    HTTPException)
from controller.security import (
    JWTBearer,
    getCurrentUserName)
from entity.biometrics import Biometrics
from entity.frequency import Frequency
from util.image import checkUploadedImage
from recognition.findFace import findFace
from recognition.faceRecognition import verifyFace
from database import biometrics as biometryDB, frequency
from database import frequency as frequencyDB
from database import user as userDB
from util.files import createUserImagesPath, removeAllFilesInFolder

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


@router.post("", dependencies=[Depends(JWTBearer())])
async def createBiometry(biometry:Biometrics) -> dict:
    id = biometryDB.create(biometry)
    return {
        "id": id
    }

@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def updateBiometry(id:int, biometry:Biometrics)-> dict:
    
    biometryDB.update(id, biometry)
    return{
        "result": "success"
    }

'''@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def deleteBiometry(id:int) -> dict:
    biometryDB.delete(id)
    return{
         "result": "success"
     }
'''
@router.put("/desabilitar/{biometryID}", dependencies=[Depends(JWTBearer())])
async def disableBiometry(biometryID:int, request:Request) -> Dict:
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator:
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
