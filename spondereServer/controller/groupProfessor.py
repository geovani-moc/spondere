from typing import Optional
from fastapi import (
    APIRouter,
    Body, 
    Depends, 
    Request)
from controller.security import (
    JWTBearer, 
    getCurrentUserName,
    getCurrentUserType)
from database import groupProfessor as groupDB
from entity.groupProfessor import GroupProfessor
from fastapi import HTTPException
from settings import(
    USER_TYPE_ADMIN,
    USER_TYPE_PROFESSOR,
    USER_TYPE_STUDENT
)

router = APIRouter()

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def readGroupByGroup(request:Request, id:int):
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN and userType != USER_TYPE_PROFESSOR:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")
    groups = groupDB.readByGroup(id)
    return {
        "Groups": groups
    }

@router.get("", dependencies=[Depends(JWTBearer())])
async def readGroupByProfessor(request:Request, username:Optional[str]=None):
    authorization = request.headers.get("authorization")
    currentUsername = getCurrentUserName(authorization)
    userType = getCurrentUserType(authorization)

    if currentUsername != username and userType != USER_TYPE_ADMIN:
         raise HTTPException(status_code=401,
            detail="O usuário não tem pode acessar a turma de outro professor.")

    if userType != USER_TYPE_ADMIN and userType != USER_TYPE_PROFESSOR:
        raise HTTPException(status_code=401,
            detail="O usuário não tem privilegio de administrador ou professor.")

    if username == None:
        return {"professor":None}
    professors = groupDB.readByUser(username)
    return {
        "professor": professors
    }

@router.post("/", dependencies=[Depends(JWTBearer())])
async def createGroup(group:GroupProfessor, request:Request):
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")
    
    groupDB.create(group)
    return {
        "result": "success"
    }

@router.put("/", dependencies=[Depends(JWTBearer())])
async def updateGroup(request:Request, group:GroupProfessor, new:GroupProfessor):
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")

    groupDB.update(new, group)

    return {
        "result": "success"
    }

@router.delete("/", dependencies=[Depends(JWTBearer())])
async def deleteGroup(request:Request, id:int = Body(...), professor:str = Body(...)):
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")

    groupDB.delete(id, professor)
    return{
        "result": "success"
    }