import logging
from typing import Dict
from psycopg2.extras import RealDictCursor
from entity.biometrics import Biometrics
from fastapi import HTTPException
import psycopg2 as pg
from datetime import datetime
from config import(
    DB_NAME,
    DB_PASSWORD,
    DB_USERNAME, 
    HOST,
    PORT
)
from settings import TIMEZONE_API_SERVER

def create(biometric: Biometrics):
    biometric.createDate = str(datetime.now())+str(TIMEZONE_API_SERVER)

    sqlQuery = 'insert into biometrics (studentID, createdate, active,\
    invalid, failure) values(%s, %s, %s, %s, %s) returning id;'
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
            (biometric.studentID,
            biometric.createDate,
            biometric.active,
            biometric.invalid,
            biometric.failure))
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

def update(id:int, biometric: Biometrics):
    sqlQuery = 'update biometrics set studentid=%s, \
        active=%s, invalid=%s, failure=%s where id=%s;'

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
            (biometric.studentID,
            biometric.active,
            biometric.invalid,
            biometric.failure, id))

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
    sqlQuery = 'select id, studentID, createdate, active, invalid, failure \
        from biometrics where id=%s;'
    biometric = Biometrics()
    
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
        (biometric.id, biometric.studentID,
        biometric.createDate, biometric.active,
        biometric.invalid, biometric.failure) = cursor.fetchone()

        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.")
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return biometric

def delete(id:int):
    sqlQuery = 'delete from biometrics where id = %s;'

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

def disable(id:int):
    sqlQuery = 'update biometrics set active=false where id=%s returning studentid;'
    studentID:int = 0
    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute(sqlQuery, (id, ))
        studentID = cursor.fetchone()[0]
        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return studentID

def existValidBiometry(studentID:int) -> bool:
    sqlQuery = 'select count(*) from biometrics where studentID=%s \
        and active=true and invalid=false;'
    count = 0
    
    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )

        cursor = connection.cursor()
        cursor.execute(sqlQuery, (studentID,))
        count = cursor.fetchone()[0]

        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.")
    finally:
        if (connection):
            cursor.close()
            connection.close()

    if count > 0: return True
    return False

def invalidate(id:int, failure:str):
    sqlQuery = 'update biometrics set invalid=true, failure=%s where id=%s;'

    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute(sqlQuery, (failure, id))

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

def validate(id:int):
    sqlQuery = 'update biometrics set invalid=false, failure=null where id=%s;'

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

def isValid(studentID:int) -> Dict:
    sqlQuery = 'select id as "biometryID", failure as "biometryError" \
    from biometrics where studentID=%s and active=true;'
    
    result = None
    
    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )

        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sqlQuery, (studentID,))
        result = cursor.fetchone()

        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.")
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return result
