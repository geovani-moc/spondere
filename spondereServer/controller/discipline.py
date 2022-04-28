from typing import Dict
from fastapi import (
    APIRouter, 
    Depends, 
    Request)
from controller.security import (
    JWTBearer,
    getCurrentUserName,
    getCurrentUserType)
from database import discipline as disciplineDB
from entity.discipline import Discipline
from fastapi import HTTPException
from settings import(
    USER_TYPE_ADMIN,
    USER_TYPE_PROFESSOR,
    USER_TYPE_STUDENT
)

router = APIRouter()

@router.post("/", dependencies=[Depends(JWTBearer())])
async def createDiscipline(discipline:Discipline, request:Request) -> Dict:
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN and userType != USER_TYPE_PROFESSOR:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")
    
    id = disciplineDB.create(discipline)

    return {
        "id": id
    }

@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def updateDiscipline(id:int, discipline:Discipline, request:Request) -> Dict:
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN and userType != USER_TYPE_PROFESSOR:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")

    disciplineDB.update(id, discipline)
    return {
        "result": "success"
    }

@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def deleteDiscipline(id:int, request:Request) -> Dict:
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")

    try:    
        disciplineDB.delete(id)
    except Exception as e:
        print(f'Erro ao tentar apagar a disciplina com id {id}.')
        return{
            "result": "Error: bd001"
        }
    return{
        "result": "success"
    }

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def readDiscipline(id:int) -> Dict:   
    discipline = disciplineDB.read(id=id)
    return {
        "discipline": discipline
    }

@router.get("/professor/", dependencies=[Depends(JWTBearer())])
async def readActiveDisciplineByProfessor(professorUsername:str, request:Request)-> Dict:
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    userType = getCurrentUserType(authorization)
    
    if username != professorUsername and userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou não é o pofessor.")

    disciplines, groups = disciplineDB.readActiveByProfessor(professorUsername)

    return{
        "discipline": disciplines,
        "group": groups
    }

@router.get("/aluno/", dependencies=[Depends(JWTBearer())])
async def readActiveDisciplineByStudent(studentUsername:str, request:Request)-> Dict:
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    userType = getCurrentUserType(authorization)

    if username != studentUsername and userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou não é o pofessor.")

    disciplines, groups = disciplineDB.readActiveByStudent(studentUsername)

    return{
        "discipline": disciplines,
        "group": groups
    }