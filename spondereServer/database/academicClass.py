from entity.academicClass import AcademicClass
from fastapi import HTTPException
import psycopg2 as pg
from config import(
    DB_NAME,
    DB_PASSWORD,
    DB_USERNAME, 
    HOST,
    PORT
)

def create(academicClass: AcademicClass):
    sqlQuery = 'insert into academicclass (groupid, titleclass, descriptionclass, \
        begindate, enddate, validationstatus, validationtype, validationcode) values\
        (%s, %s, %s, %s, %s, %s, %s, %s ) returning id;'
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
            academicClass.validationStatus,
            academicClass.validationType,
            academicClass.validationCode))
        id = cursor.fetchone()[0]

        connection.commit()

    except:
        raise HTTPException(status_code=406,
                detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return id

def update(id:int, academicClass: AcademicClass):
    sqlQuery = 'update academicclass set groupid=%s, titleclass=%s,\
    descriptionclass=%s, begindate=%s, enddate=%s, validationstatus=%s,\
    validationtype=%s, validationcode=%s where id = %s;'

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
            academicClass.validationStatus,
            academicClass.validationType,
            academicClass.validationCode,
            id))

        connection.commit()

    except:
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return None

def read(id: int):
    sqlQuery = 'select id, groupid, titleclass, descriptionclass, begindate, enddate,\
        validationstatus, validationtype, validationcode from academicclass where id = %s;'
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
        () = cursor.fetchone()

        connection.commit()

    except:
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.")
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return academicClass

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

    except:
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return None