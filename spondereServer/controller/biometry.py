from typing import Dict
from fastapi import (
    APIRouter, 
    Depends,
    File, 
    UploadFile,
    HTTPException,
    Request)
from controller.security import (
    JWTBearer,
    getCurrentUserName)
from entity.biometrics import Biometrics
from util.image import checkUploadedImage
from recognition.findFace import findFace
from recognition.faceRecognition import verifyFace
from database import biometrics as biometryDB

router = APIRouter()

@router.post("/checar", dependencies=[Depends(JWTBearer())])
async def checkBiometry(request:Request, file: UploadFile = File(...))->Dict:
    authorization = request.headers.get("authorization")
    userName = getCurrentUserName(authorization)

    contents = await file.read()
    image = checkUploadedImage(contents)

    result:bool = False

    if image is None: return {"recognition": False,"error": "sem imagem"}

    face, error = findFace(image)
    if error:
        raise HTTPException(status_code=500,
            detail="Erro no sistema de reconhecimento facial: \n" + error) 
    
    if error is None:
        result = verifyFace(face, userName)
        #salvar face(frequencia) --await
        if not result: return{"recognition": result, "error":"Face não definida."}

    return {"recognition": result, "error": None}

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
