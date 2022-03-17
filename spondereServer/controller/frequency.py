import logging
from typing import Dict
from fastapi import (
    APIRouter,
    Depends, 
    Request, 
    Body)
from controller.security import (
    JWTBearer,
    getCurrentUserName)
from database import frequency as frequencyDB
from database import groupStudent as groupStudentDB
from entity.frequency import Frequency, FrequencyList
from database import user as userDB
from fastapi import HTTPException

router = APIRouter()

@router.post("/", dependencies=[Depends(JWTBearer())])
async def createFrequency(frequency:Frequency, request:Request) -> Dict:
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")
     
    id = frequencyDB.create(frequency)
    return {
        "id": id
    }

@router.post("/manual", dependencies=[Depends(JWTBearer())])
async def createManualFrequency(request:Request, academicClassID:int = Body(...), studentID:int = Body(...)) -> Dict:
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator and not user.professor:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")

    frequency = Frequency()
    frequency.academicClassID = academicClassID
    frequency.studentID = studentID
    frequency.ManualAttendance = True
    frequency.BLEAttendance = False
    frequency.QrCodeAttendance = False
         
    id = frequencyDB.create(frequency)
    return {
        "id": id
    }

@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def updateFrequency(id:int, frequency:Frequency, request:Request) -> Dict:
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador.")

    frequencyDB.update(id, frequency)
    return {
        "result": "success"
    }

@router.delete("/{id}", dependencies=[Depends(JWTBearer())])
async def deleteFrequency(id:int, request:Request) -> Dict:
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator and not user.professor:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")
    
    frequencyDB.delete(id)
    return{
        "result": "success"
    }

@router.get("/{id}", dependencies=[Depends(JWTBearer())])
async def readFrequency(id:int) -> Dict:   
    frequency = frequencyDB.read(id)
    return {
        "frequency": frequency
    }

@router.get("/grupo/", dependencies=[Depends(JWTBearer())])
async def readFrequencybyGroup(academicClassID:int, groupID:int, request:Request) -> Dict:
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator and not user.professor:
        raise HTTPException(status_code=401,
            detail="O usuario não tem privilegio de administrador ou professor.")   
    studentsPresents = frequencyDB.studentsPresents(academicClassID)
    studentsByGroup = groupStudentDB.readStudentsIDbyGroup(groupID)
    
    attendanceList = createAttendanceList(groupID, studentsPresents, studentsByGroup)

    return {
        "frequencyList": attendanceList
    }

def createAttendanceList(groupID:int, presents, groupStudents):
    result = []
    
    for (studentID, fullName) in groupStudents:
        presence = False
        frequencyList = FrequencyList()

        for (id, frequencyID, manualAttendance) in presents:
            if id == studentID:
                frequencyList.groupID = groupID
                frequencyList.studentID = studentID
                frequencyList.fullName = fullName
                frequencyList.frequencyID = frequencyID
                frequencyList.isManual = manualAttendance
                result.append(frequencyList)
                presence = True

        if not presence:
            frequencyList.groupID = groupID
            frequencyList.studentID = studentID
            frequencyList.fullName = fullName
            frequencyList.frequencyID = None
            frequencyList.isManual = False
            result.append(frequencyList)
        

    return result

@router.get("/aluno/", dependencies=[Depends(JWTBearer())])
async def isPresent(academicClassID:int, studentID:int) -> Dict: 
    try:  
        (id, failure, validationCode) = frequencyDB.attendancePerStudent(academicClassID, studentID)
    except:
        logging.error("Nehuma frequencia encontrada com os dados fornecidos.")
        raise HTTPException(status_code=403,
                detail="f001")

    return {
        "id": id,
        "failure": failure,
        "code": validationCode
    }
