from typing import Dict
from fastapi import (
    APIRouter, 
    Depends, 
    Request)
from controller.security import (
    JWTBearer,
    getCurrentUserName)
from database import frequency as frequencyDB
from entity.frequency import Frequency
from database import user as userDB
from fastapi import HTTPException

router = APIRouter()

@router.post("/", dependencies=[Depends(JWTBearer())])
async def createFrequency(frequency:Frequency) -> Dict:   
    id = frequencyDB.create(frequency)
    return {
        "id": id
    }

@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def updateFrequency(id:int, frequency:Frequency, request:Request) -> Dict:
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")

    frequencyDB.update(id, frequency)
    return {
        "result": "success"
    }

@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def deleteFrequency(id:int, request:Request) -> Dict:
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")
    
    frequencyDB.delete(id)
    return{
        "result": "success"
    }

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def readFrequency(id:int) -> Dict:   
    frequency = frequencyDB.read(id=id)
    return {
        "frequency": frequency
    }

