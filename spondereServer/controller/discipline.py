from fastapi import (
    APIRouter, 
    Depends)
from controller.security import (
    JWTBearer)
from database import discipline as disciplineDB
from entity.discipline import Discipline

router = APIRouter()

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def readDiscipline(id:int):
    discipline = disciplineDB.read(id=id)
    return {
        "discipline": discipline
    }

@router.post("", dependencies=[Depends(JWTBearer())])
async def createDiscipline(discipline:Discipline):
    id = disciplineDB.create(discipline)

    return {
        "id": id
    }

@router.put("/{id}", dependencies=[Depends(JWTBearer)])
async def updateDiscipline(id:int, discipline:Discipline):
    disciplineDB.update(id, discipline)

    return {
        "result": "success"
    }

@router.delete("/{id}", dependencies=[Depends(JWTBearer)])
async def deleteDiscipline(id:int):
    disciplineDB.delete(id)
    return{
        "result": "success"
    }