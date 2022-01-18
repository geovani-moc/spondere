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
from util.image import checkUploadedImage
from recognition.findFace import findFace
from recognition.faceRecognition import verifyFace

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
