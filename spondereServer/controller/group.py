from fastapi import (
    APIRouter, 
    Depends, 
    Request)
from controller.security import (
    JWTBearer, 
    getCurrentUserName)
from database import group as groupDB
from entity.group import Group
from database import user as userDB
from fastapi import HTTPException

router = APIRouter()

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def readGroup(id:int):
    group = groupDB.read(id)
    return {
        "Group": group
    }

@router.post("", dependencies=[Depends(JWTBearer())])
async def createGroup(group:Group, request:Request):
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

@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def updateGroup(id:int, group:Group, request:Request):
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")
    groupDB.update(id, group)

    return {
        "result": "success"
    }

@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def deleteGroup(id:int, request:Request):
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")

    groupDB.delete(id)
    return{
        "result": "success"
    }