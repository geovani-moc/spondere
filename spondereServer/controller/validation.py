import logging
from fastapi import (
    APIRouter, 
    Depends, 
    Request, 
    Body)
from controller.security import JWTBearer, getCurrentUserName, getCurrentUserType
from database import academicClass as classDB
from fastapi import HTTPException
from util.validation import generateValidationCode
from settings import(
    USER_TYPE_ADMIN,
    USER_TYPE_PROFESSOR,
    USER_TYPE_STUDENT
)

router = APIRouter()

@router.post("/criar", dependencies=[Depends(JWTBearer())])
async def startClassAttendance(request:Request, academicClassID:int = Body(...)):
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN and userType != USER_TYPE_PROFESSOR:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")

    if(not classAttendanceIsValidToBegin(academicClassID)):
        raise HTTPException(status_code=406,
            detail="Uma aula não pode ser iniciada mais de uma vez.")
    
    validationCode = generateValidationCode()
    
    if classDB.setValidationCode(academicClassID, validationCode):
        logging.info("Aula iniciada, id da aula: "+ str(academicClassID)+",\
             codigo de valição: "+ validationCode )
    else:
        raise HTTPException(status_code=406,
            detail="Código não existe, ou não é válido ou já existe código cadastrado.")

    return {
        "validationCode":validationCode
    }

def classAttendanceIsValidToBegin(academicClassID:int) -> bool:
    academicClass = classDB.read(academicClassID)

    if academicClass.blockedAttendance:
        return False
    
    if academicClass.endDate == None:
        return False

    return True

@router.post("/verificar/", dependencies=[Depends(JWTBearer())])
async def validationCode( request:Request, code:str = Body(...)):
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