from fastapi import (
    APIRouter, 
    Depends, 
    Request)
from controller.security import JWTBearer, getCurrentUserType
from entity.academicClass import AcademicClass
from database import academicClass as classDB
from fastapi import HTTPException
from settings import(
    USER_TYPE_ADMIN,
    USER_TYPE_PROFESSOR,
    USER_TYPE_STUDENT
)

router = APIRouter()
 
@router.post("/", dependencies=[Depends(JWTBearer())])
async def createAcademicClass(academicClass:AcademicClass, request:Request) -> dict:
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN and userType != USER_TYPE_PROFESSOR:
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
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN and userType != USER_TYPE_PROFESSOR:
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
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN and userType != USER_TYPE_PROFESSOR:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")

    try:    
        classDB.delete(id)
    except Exception as e:
        print(f'Erro ao tentar apagar a aula com id {id}.')
        return{
            "result": "Error: bd001"
        }

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
async def updateBlockedAcademicClass(request:Request, academicClassID:int)-> dict:
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN and userType != USER_TYPE_PROFESSOR:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")

    classDB.blockAttendance(academicClassID)
    return{
        "result": "success"
    }