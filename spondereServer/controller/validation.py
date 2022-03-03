import logging
from fastapi import (
    APIRouter, 
    Depends, 
    Request)
from controller.security import JWTBearer, getCurrentUserName
from database import academicClass as classDB
from database import user as userDB
from fastapi import HTTPException
from util.validation import generateValidationCode

router = APIRouter()

@router.get("/criar/", dependencies=[Depends(JWTBearer())])
async def startClassAttendance(classID:int, request:Request):
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator and not user.professor:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")
    
    validationCode = generateValidationCode()
    
    if classDB.setValidationCode(classID, validationCode):
        logging.info("Aula iniciada, id da aula: "+ str(classID)+",\
             codigo de valição: "+ validationCode )
    else:
        raise HTTPException(status_code=406,
            detail="Código não existe, ou não é válido ou já existe código cadastrado.")

    return {
        "validationCode":validationCode
    }

@router.get("/verificar/", dependencies=[Depends(JWTBearer())])
async def validationCode(code:str, request:Request):
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)

    classID:int = classDB.getActiveClassIDByCode(code, username)
    
    if classID > 0:
        logging.info("Codigo de aula verificado com sucesso: " + code)
    else:
        raise HTTPException(status_code=406,
            detail="Código não existe ou não é válido.")

    return {
        "classID": classID
    }