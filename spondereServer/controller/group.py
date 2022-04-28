from fastapi import (
    APIRouter, 
    Depends, 
    Request)
from controller.security import (
    JWTBearer, 
    getCurrentUserType)
from database import group as groupDB
from entity.group import Group
from fastapi import HTTPException
from settings import(
    USER_TYPE_ADMIN,
    USER_TYPE_PROFESSOR,
    USER_TYPE_STUDENT
)

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
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")
    
    id = groupDB.create(group)
    return {
        "id": id
    }

@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def updateGroup(id:int, group:Group, request:Request):
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")
    groupDB.update(id, group)

    return {
        "result": "success"
    }

@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def deleteGroup(id:int, request:Request):
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")

    try:
        groupDB.delete(id)
    except Exception as e:
        print(f'Erro ao tentar apagar o grupo com id {id}.')
        return{
            "result": "Error: bd001"
        }

    return{
        "result": "success"
    }