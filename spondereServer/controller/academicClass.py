from fastapi import (
    APIRouter, 
    Depends, 
    Request)
from controller.security import JWTBearer, getCurrentUserName
from entity.academicClass import AcademicClass
from database import academicClass as classDB
from database import user as userDB
from fastapi import HTTPException

router = APIRouter()
 
@router.post("/", dependencies=[Depends(JWTBearer())])
async def createAcademicClass(academicClass:AcademicClass, request:Request) -> dict:
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator or not user.professor:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")

    id = classDB.create(academicClass)
    return {
        "id": id
    }

@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def updateAcademicClass(id:int, academicClass:AcademicClass, request:Request)-> dict:
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator or not user.professor:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")

    classDB.update(id, academicClass)
    return{
        "result": "success"
    }

@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def deleteAcademicClass(id:int, request:Request) -> dict:
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator or not user.professor:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")

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

@router.get("/grupo/", dependencies=[Depends(JWTBearer())])
async def getClassByGroupID(groupID:int):
                
    academicClasses = classDB.readByGroupID(groupID)

    return {
        "academicClass": academicClasses
    }