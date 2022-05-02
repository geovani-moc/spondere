from numpy import record
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
from util.image import checkUploadedImage, imageResized
from util.image import encodePresentStudentsImages

def create(frequency: Frequency):
    frequency.createDate = str(datetime.now())+str(TIMEZONE_API_SERVER)

    sqlQuery = 'insert into frequency (studentID, academicClassID, manualAttendance,\
    BLEAttendance, QrCodeAttendance, createDate, validationCode, latitude, longitude,\
    failure, photo) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) returning id;'
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
        
        (frequency.id, frequency.studentID, frequency.academicClassID, 
        frequency.ManualAttendance, frequency.BLEAttendance, frequency.QrCodeAttendance, 
        frequency.createDate, frequency.validationCode, frequency.latitude, 
        frequency.longitude, frequency.failure, frequency.photo) = cursor.fetchone()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return frequency

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

def studentsPresents(academicClassID:int):
    sqlQuery = 'select u.id, f.id, f.manualattendance from users u \
    inner join frequency f on f.studentid = u.id \
    and f.academicclassid = %s and f.failure is null;'

    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )

        cursor = connection.cursor()
        cursor.execute(sqlQuery, (academicClassID,))
        
        records = cursor.fetchall()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return records

def attendancePerStudent(academicClassID:int, studentID:int):
    sqlQuery = 'select f.id, f.failure from frequency f \
    where f.academicclassid=%s and f.studentid=%s\
    order by createdate desc limit 1;'

    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )

        cursor = connection.cursor()
        cursor.execute(sqlQuery, (academicClassID, studentID))
        record = cursor.fetchone()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return record

def studentsPresentsWithPhoto(academicClassID:int):
    sqlQuery = 'select u.fullname, f.photo from frequency f\
        inner join users u on f.academicclassid = %s\
        and u.id = f.studentid and failure is null;'

    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )

        cursor = connection.cursor()
        cursor.execute(sqlQuery, (academicClassID,))
        
        records = cursor.fetchall()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return compactPresentStudentsImages(records)

def compactPresentStudentsImages(records):
    usernames = []
    images = []
    for (username, file) in records:
        image = checkUploadedImage(file)
        if file != None:
            scale = 100.0 / image.shape[0]
            width = int(image.shape[1] * scale)
            height = int(image.shape[0] * scale)
            image = imageResized(image, height, width)

        usernames.append(username)
        images.append(image)


    return encodePresentStudentsImages(usernames, images)

def attendanceRate(classID:int):
    sqlQuery = 'select count(*) from academicclass a\
        inner join \"groups\" g on a.id=%s and a.groupid=g.id\
        inner join group_students gs  on gs.groupid = g.id union\
        select count(*) from frequency f where academicclassid=%s and failure is null;'

    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )

        cursor = connection.cursor()
        cursor.execute(sqlQuery, (classID, classID,))
        
        records = cursor.fetchall()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return records[0][0], records[1][0]