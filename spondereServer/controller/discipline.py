from typing import Dict
from fastapi import (
    APIRouter, 
    Depends, 
    Request)
from controller.security import (
    JWTBearer,
    getCurrentUserName)
from database import discipline as disciplineDB
from entity.discipline import Discipline
from database import user as userDB
from fastapi import HTTPException

router = APIRouter()

@router.post("", dependencies=[Depends(JWTBearer())])
async def createDiscipline(discipline:Discipline, request:Request) -> Dict:
    authorization = request.headers.get("authorization")
    userName = getCurrentUserName(authorization)
    user = userDB.read(userName)

    if not user.administrator or not user.professor:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")
    
    id = disciplineDB.create(discipline)

    return {
        "id": id
    }

@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def updateDiscipline(id:int, discipline:Discipline, request:Request) -> Dict:
    authorization = request.headers.get("authorization")
    userName = getCurrentUserName(authorization)
    user = userDB.read(userName)

    if not user.administrator or not user.professor:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")

    disciplineDB.update(id, discipline)
    return {
        "result": "success"
    }

@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def deleteDiscipline(id:int, request:Request) -> Dict:
    authorization = request.headers.get("authorization")
    userName = getCurrentUserName(authorization)
    user = userDB.read(userName)

    if not user.administrator or not user.professor:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")
    
    disciplineDB.delete(id)
    return{
        "result": "success"
    }

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def readDiscipline(id:int) -> Dict:   
    discipline = disciplineDB.read(id=id)
    return {
        "discipline": discipline
    }
