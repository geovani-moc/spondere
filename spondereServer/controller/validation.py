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

@router.post("/criar/{ClassID}", dependencies=[Depends(JWTBearer())])
async def startClassAttendance(classID:int, request:Request):
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator or not user.professor:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")
    
    validationCode = generateValidationCode()
    
    if classDB.setValidationCode(classID, validationCode):
        logging.info("Aula iniciada, id da aula: "+classID+",\
             codigo de valição: "+ validationCode )

    return {
        "validationCode":validationCode
    }

@router.get("/verificar/{code}", dependencies=[Depends(JWTBearer())])
async def validationCode(classID:int, request:Request):
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)
    
    validationCode = generateValidationCode()
    
    if classDB.setValidationCode(classID, validationCode):
        logging.info("Aula iniciada, id da aula: "+classID+",\
             codigo de valição: "+ validationCode )

    return {
        "validationCode":validationCode
    }