from typing import Optional
from fastapi import (
    APIRouter,
    Body, 
    Depends, 
    Request)
from controller.security import (
    JWTBearer, 
    getCurrentUserName)
from database import groupProfessor as groupDB
from entity.groupProfessor import GroupProfessor
from database import user as userDB
from fastapi import HTTPException

router = APIRouter()

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def readGroupByGroup(request:Request, id:int):
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator and not user.professor:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")
    groups = groupDB.readByGroup(id)
    return {
        "Groups": groups
    }

@router.get("", dependencies=[Depends(JWTBearer())])
async def readGroupByProfessor(request:Request, username:Optional[str]=None):
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator and not user.professor:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")

    if username == None:
        return {"professor":None}
    professors = groupDB.readByUser(username)
    return {
        "professor": professors
    }

@router.post("", dependencies=[Depends(JWTBearer())])
async def createGroup(group:GroupProfessor, request:Request):
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")
    
    id = groupDB.create(group)
    return {
        "id": id
    }

@router.put("/", dependencies=[Depends(JWTBearer())])
async def updateGroup(request:Request, group:GroupProfessor, new:GroupProfessor):
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")

    groupDB.update(new, group)

    return {
        "result": "success"
    }

@router.delete("/", dependencies=[Depends(JWTBearer())])
async def deleteGroup(request:Request, id:int = Body(...), professor:str = Body(...)):
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")

    groupDB.delete(id, professor)
    return{
        "result": "success"
    }