from entity.frequency import Frequency
import logging
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

def create(frequency: Frequency):
    frequency.createDate = str(datetime.datetime.now())+str(TIMEZONE_API_SERVER)

    sqlQuery = 'insert into frequency (studentID, academicClassID, manualAttendance,\
    BLEAttendance, QrCodeAttendance, createDate, validationCode, latitude, longitude,\
    failure, photo) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s),'
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
            (frequency.studentID, frequency.academicClassID, frequency.ManualAttendance,
            frequency.BLEAttendance, frequency.QrCodeAttendance, frequency.createDate, 
            frequency.validationCode, frequency.latitude, frequency.longitude, frequency.failure, 
            frequency.photo))

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

def read(id:int):
    sqlQuery = 'select id, studentID, academicClassID, manualAttendance,\
    BLEAttendance, QrCodeAttendance, createDate, validationCode,\
    latitude, longitude, failure, photo from frequency where id = %s;'
    frequency = Frequency()
    
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
        
        (frequency.studentID, frequency.academicClassID, frequency.ManualAttendance,
            frequency.BLEAttendance, frequency.QrCodeAttendance, frequency.createDate, 
            frequency.validationCode, frequency.latitude, frequency.longitude, frequency.failure, 
            frequency.photo) = cursor.fetchone()

        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return Frequency

def update(id:int, frequency: Frequency):
    sqlQuery = 'update frequency set studentID=%s, academicClassID=%s, manualAttendance=%s,\
    BLEAttendance=%s, QrCodeAttendance=%s, createDate=%s, validationCode=%s,\
    latitude=%s, longitude=%s, failure=%s, photo=%s where id=%s;'
    
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
            ((frequency.studentID, frequency.academicClassID, frequency.ManualAttendance,
            frequency.BLEAttendance, frequency.QrCodeAttendance, frequency.createDate, 
            frequency.validationCode, frequency.latitude, frequency.longitude, frequency.failure, 
            frequency.photo, id)))
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

def delete(id: int):
    sqlQuery = 'delete from frequency where id = %s;'
    
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