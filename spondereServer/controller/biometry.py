from typing import Dict
from fastapi import (
    APIRouter, 
    Depends,
    File, 
    UploadFile,
    Request, 
    BackgroundTasks)
from controller.security import (
    JWTBearer,
    getCurrentUserName)
from entity.biometrics import Biometrics
from entity.frequency import Frequency
from util.image import checkUploadedImage
from recognition.findFace import findFace
from recognition.faceRecognition import verifyFace
from database import biometrics as biometryDB
from database import frequency as frequencyDB

router = APIRouter()

@router.post("/checar/", dependencies=[Depends(JWTBearer())])
async def checkBiometry(data:Frequency, request:Request, file: UploadFile = File(...))->Dict:
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    contents = await file.read()
    BackgroundTasks.add_task(processBiometrics, data, username, contents)

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

@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def deleteBiometry(id:int) -> dict:
    biometryDB.delete(id)
    return{
         "result": "success"
     }

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def getBiometry(id:int) -> dict:
    biometry = biometryDB.read(id)
    return {
        "biometry": biometry
    }
