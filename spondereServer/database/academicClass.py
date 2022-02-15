import logging
from typing import Dict
from entity.academicClass import AcademicClass
from fastapi import HTTPException
import psycopg2 as pg
from psycopg2.extras import RealDictCursor
from config import(
    DB_NAME,
    DB_PASSWORD,
    DB_USERNAME, 
    HOST,
    PORT
)

def create(academicClass: AcademicClass):
    sqlQuery = 'insert into academicclass (groupid, titleclass, descriptionclass, begindate,\
    enddate, activevalidation , validationbyqrcode, validationbyble, validationcode)\
    values (%s, %s, %s, to_timestamp(%s, %s), to_timestamp(%s, %s), %s, %s, %s, %s) returning id;'
    
    id = None
    datetimeFormat = 'dd-mm-yyyy HH24:MI'

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
            datetimeFormat,
            academicClass.endDate,
            datetimeFormat,
            academicClass.activeValidation,
            academicClass.validationByQrCode,
            academicClass.validationByBLE,
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

def update(id:int, academicClass: AcademicClass):
    sqlQuery = 'update academicclass set groupid=%s, titleclass=%s,\
    descriptionclass=%s, begindate=to_timestamp(%s, %s), enddate=to_timestamp(%s, %s),\
    activevalidation=%s, validationbyqrcode=%s, validationbyble=%s, validationcode=%s \
    where id=%s;'
    datetimeFormat = 'dd-mm-yyyy HH24:MI'
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
            datetimeFormat,
            academicClass.endDate,
            datetimeFormat,
            academicClass.activeValidation,
            academicClass.validationByQrCode,
            academicClass.validationByBLE,
            academicClass.validationCode,
            id))

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
    activevalidation , validationbyqrcode, validationbyble, validationcode \
    from academicclass where id=%s;'
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
        academicClass.activeValidation,
        academicClass.validationByQrCode,
        academicClass.validationByBLE,
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
        a.enddate, a.activevalidation, a.validationbyqrcode, a.validationbyble, a.validationcode \
        from academicclass a where a.groupid = %s;'
    
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
    #testar o sql
    sqlQuery = 'update academicclass set validationcode=%s where id=%s;'

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

def getActiveClassIDByCode(validationCode:str) -> bool:
    #atualizar o sql
    sqlQuery = ''

    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute(sqlQuery, (validationCode,))
        id = cursor.fetchone()
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