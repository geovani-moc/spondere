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

    if not user.administrator and not user.professor:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")

    id = classDB.create(academicClass)
    return {
        "id": id
    }

@router.put("/", dependencies=[Depends(JWTBearer())])
async def updateAcademicClass(academicClass:AcademicClass, request:Request)-> dict:
    if academicClass.id < 1:
        raise HTTPException(status_code=401,
            detail="Aula inválida.")
    
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator and not user.professor:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")

    if(academicClass.blockedAttendance):
        classDB.updateBlocked(academicClass)
    else:
        classDB.update(academicClass)
        
    return{
        "result": "success"
    }

@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def deleteAcademicClass(id:int, request:Request) -> dict:
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator and not user.professor:
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

@router.put("/bloquear/", dependencies=[Depends(JWTBearer())])
async def updateAcademicClass(request:Request, academicClassID:int)-> dict:
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator and not user.professor:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")

    classDB.blockAttendance(academicClassID)
    return{
        "result": "success"
    }