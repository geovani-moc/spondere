from typing import Optional
from fastapi import (
    APIRouter,
    Body, 
    Depends, 
    Request)
from controller.security import (
    JWTBearer, 
    getCurrentUserType)
from database import groupStudent as groupDB
from entity.groupStudent import GroupStudent
from fastapi import HTTPException
from settings import(
    USER_TYPE_ADMIN,
    USER_TYPE_PROFESSOR,
    USER_TYPE_STUDENT
)


router = APIRouter()

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def readGroupByGroup(id:int):
    groups = groupDB.readByGroup(id)
    return {
        "group": groups
    }

@router.get("", dependencies=[Depends(JWTBearer())])
async def readGroupByStudent(username:Optional[str]=None):
    if username == None:
        return {"Students":None}
    students = groupDB.readByUser(username)
    return {
        "student": students
    }

@router.post("/", dependencies=[Depends(JWTBearer())])
async def createGroup(group:GroupStudent, request:Request):
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuário não tem privilegio de administrador.")
    
    groupDB.create(group)
    return {
        "result": "success"
    }

@router.put("/", dependencies=[Depends(JWTBearer())])
async def updateGroup(request:Request, group:GroupStudent, new:GroupStudent):
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
async def deleteGroup(request:Request, id:int = Body(...), student:str = Body(...)):
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")

    groupDB.delete(id, student)
    return{
        "result": "success"
    }