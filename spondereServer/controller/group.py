from fastapi import (
    APIRouter, 
    Depends)
from controller.security import (
    JWTBearer)
from database import group as groupDB
from entity.group import Group

router = APIRouter()

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def readGroup(id:int):
    group = groupDB.read(id)
    return {
        "Group": group
    }

@router.post("", dependencies=[Depends(JWTBearer())])
async def createGroup(group:Group):
    id = groupDB.create(group)

    return {
        "id": id
    }

@router.put("/{id}", dependencies=[Depends(JWTBearer)])
async def updateGroup(id:int, group:Group):
    groupDB.update(id, group)

    return {
        "result": "success"
    }

@router.delete("/{id}", dependencies=[Depends(JWTBearer)])
async def deleteGroup(id:int):
    groupDB.delete(id)
    return{
        "result": "success"
    }