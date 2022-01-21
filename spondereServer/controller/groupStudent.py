from typing import Optional
from fastapi import (
    APIRouter,
    Body, 
    Depends, 
    Request)
from controller.security import (
    JWTBearer, 
    getCurrentUserName)
from database import groupStudent as groupDB
from entity.groupStudent import GroupStudent
from database import user as userDB
from fastapi import HTTPException

router = APIRouter()

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def readGroupByGroup(id:int):
    groups = groupDB.readByGroup(id)
    return {
        "Groups": groups
    }

@router.get("", dependencies=[Depends(JWTBearer())])
async def readGroupByStudent(username:Optional[str]=None):
    if username == None:
        return {"Students":None}
    students = groupDB.readByUser(username)
    return {
        "Students": students
    }

@router.post("", dependencies=[Depends(JWTBearer())])
async def createGroup(group:GroupStudent, request:Request):
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
async def updateGroup(request:Request, group:GroupStudent, new:GroupStudent):
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
async def deleteGroup(request:Request, id:int = Body(...), student:str = Body(...)):
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")

    groupDB.delete(id, student)
    return{
        "result": "success"
    }