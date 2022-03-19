from fastapi import (
    APIRouter, 
    Depends,
    Request)
from controller.security import (
    JWTBearer,
    getCurrentUserType)
from database import period as periodDB
from entity.period import Period 
from fastapi import HTTPException
from settings import(
    USER_TYPE_ADMIN,
    USER_TYPE_PROFESSOR,
    USER_TYPE_STUDENT
)

router = APIRouter()

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def readPeriod(id:int):
    period = periodDB.read(id)
    return {
        "Period": period
    }

@router.post("", dependencies=[Depends(JWTBearer())])
async def createPeriod(period:Period, request:Request):
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")
    
    id = periodDB.create(period)

    return {
        "id": id
    }

@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def updatePeriod(id:int, period:Period, request:Request):
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")
    
    periodDB.update(id, period)
    return {
        "result": "success"
    }

@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def deletePeriod(id:int, request:Request):
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")
    
    periodDB.delete(id)
    return{
        "result": "success"
    }