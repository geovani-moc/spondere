from fastapi import (
    APIRouter, 
    Depends)
from controller.security import (
    JWTBearer)
from entity.academicClass import AcademicClass
from database import academicClass as classDB, discipline

router = APIRouter()
 

@router.post("", dependencies=[Depends(JWTBearer())])
async def createAcademicClass(academicClass:AcademicClass) -> dict:
    id = classDB.create(academicClass)
    return {
        "id": id
    }

@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def updateAcademicClass(id:int, academicClass:AcademicClass)-> dict:
    classDB.update(id, academicClass)
    return{
        "result": "success"
    }

@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def deleteAcademicClass(id:int) -> dict:
    classDB.delete(id)
    return{
         "result": "success"
     }

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def getAcademicClass(id:int) -> dict:
    academicClass = classDB.read(id)
    return {
        "academicClass": academicClass
    }