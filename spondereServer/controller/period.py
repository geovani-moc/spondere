from fastapi import (
    APIRouter, 
    Depends)
from controller.security import (
    JWTBearer)
from database import period as periodDB
from entity.period import Period 

router = APIRouter()

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def readPeriod(id:int):
    period = periodDB.read(id)
    return {
        "Period": period
    }

@router.post("", dependencies=[Depends(JWTBearer())])
async def createPeriod(period:Period):
    id = periodDB.create(period)

    return {
        "id": id
    }

@router.put("/{id}", dependencies=[Depends(JWTBearer)])
async def updatePeriod(id:int, period:Period):
    periodDB.update(id, period)

    return {
        "result": "success"
    }

@router.delete("/{id}", dependencies=[Depends(JWTBearer)])
async def deletePeriod(id:int):
    periodDB.delete(id)
    return{
        "result": "success"
    }