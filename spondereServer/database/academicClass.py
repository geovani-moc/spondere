import logging
from typing import Dict
from entity.academicClass import AcademicClass
from fastapi import HTTPException
import psycopg2 as pg
from psycopg2.extras import RealDictCursor
from datetime import datetime
from settings import (
    TIMEZONE_API_SERVER
)
from config import(
    DB_NAME,
    DB_PASSWORD,
    DB_USERNAME, 
    HOST,
    PORT
)

def create(academicClass: AcademicClass):
    currentDate = str(datetime.now())+str(TIMEZONE_API_SERVER)
    
    sqlQuery = 'insert into academicclass (groupid, titleclass, descriptionclass,\
        begindate, enddate, createDate, lastChangeDate, longitude, latitude, \
        activevalidation , validationbyqrcode,\
        validationbyble, blockedAttendance, validationcode) \
    values (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id;'
    
    id = None

    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute(sqlQuery, 
            (academicClass.groupID,
            academicClass.titleClass,
            academicClass.descriptionClass,
            academicClass.beginDate,
            academicClass.endDate,
            currentDate,
            currentDate,
            academicClass.longitude,
            academicClass.latitude,
            academicClass.activeValidation,
            academicClass.validationByQrCode,
            academicClass.validationByBLE,
            academicClass.blockedAttendance,
            academicClass.validationCode))
        
        id = cursor.fetchone()[0]

        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
                detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return id

def update(academicClass: AcademicClass):
    currentDate = str(datetime.now())+str(TIMEZONE_API_SERVER)

    sqlQuery = 'update academicclass set groupid=%s, titleclass=%s, descriptionclass=%s,\
        begindate=%s, enddate=%s, lastChangeDate=%s, longitude=%s, latitude=%s, activevalidation=%s,\
        validationbyqrcode=%s, validationbyble=%s, blockedattendance=%s, validationcode=%s \
    where id=%s;'
 
    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute(sqlQuery, 
            (academicClass.groupID,
            academicClass.titleClass,
            academicClass.descriptionClass,
            academicClass.beginDate,
            academicClass.endDate,
            currentDate,
            academicClass.longitude,
            academicClass.latitude,
            academicClass.activeValidation,
            academicClass.validationByQrCode,
            academicClass.validationByBLE,
            academicClass.blockedAttendance,
            academicClass.validationCode,
            academicClass.id))

        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return True

def read(id: int):
    sqlQuery = 'select id, groupid, titleclass, descriptionclass, begindate, enddate,\
    longitude, latitude, activevalidation , validationbyqrcode, validationbyble,\
    blockedAttendance, validationcode from academicclass where id=%s;'
    academicClass = AcademicClass()
    
    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )

        cursor = connection.cursor()
        cursor.execute(sqlQuery, (id,))
        (academicClass.id,
        academicClass.groupID,
        academicClass.titleClass,
        academicClass.descriptionClass,
        academicClass.beginDate,
        academicClass.endDate,
        academicClass.longitude,
        academicClass.latitude,
        academicClass.activeValidation,
        academicClass.validationByQrCode,
        academicClass.validationByBLE,
        academicClass.blockedAttendance,
        academicClass.validationCode) = cursor.fetchone()

        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.")
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return academicClass

def readByGroupID(groupID:int) -> Dict:
    sqlQuery = 'select a.id, a.groupid, a.titleclass, a.descriptionclass, a.begindate, \
        a.enddate, a.longitude, a.latitude, a.activevalidation, a.validationbyqrcode, \
        a.validationbyble, a.blockedAttendance, a.validationcode from academicclass a \
        where a.groupid = %s order by lastChangeDate desc;'
    
    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )

        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sqlQuery, (groupID,))
        records = cursor.fetchall()
        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.")
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return records

def delete(id:int):
    sqlQuery = 'delete from academicClass where id = %s;'

    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute(sqlQuery, 
            (id,))

        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return True

def setValidationCode(id:int, validationCode:str) -> bool:
    sqlQuery = 'update academicclass set validationcode=%s, activevalidation=true \
        where id=%s and validationcode is null returning id;'

    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute(sqlQuery, (validationCode,id))
        records = cursor.fetchall()

        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()
    
    if len(records) == 0: return False

    return True

def getActiveClassIDByCode(validationCode:str, username:str) -> int:
    sqlQuery = 'select a.id from academicclass a \
    inner join \"groups\" g on a.activevalidation is true and a.validationcode=%s and a.groupid = g.id\
    inner join group_students gs on gs.studentusername=%s and gs.groupid=g.id;'

    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute(sqlQuery, (validationCode, username))
        records = cursor.fetchone()[0]
        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return records

def blockAttendance(id:int):
    sqlQuery = 'update academicclass set blockedattendance=true where id=%s;'
 
    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute(sqlQuery, (id,))

        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return True

def updateBlocked(academicClass: AcademicClass):
    sqlQuery = 'update academicclass set titleclass=%s, descriptionclass=%s where id=%s;'

    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute(sqlQuery, 
            (academicClass.titleClass,
            academicClass.descriptionClass,
            academicClass.id))

        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return True
    

def infoCheckable(classID:int):
    sqlQuery = 'select a.groupid, a.enddate from academicclass a where id=%s;'
    
    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )

        cursor = connection.cursor()
        cursor.execute(sqlQuery, (classID,))
        records = cursor.fetchone()
        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.")
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return records
