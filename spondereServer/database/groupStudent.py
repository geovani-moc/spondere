import logging
from typing import Dict, List
from entity.groupStudent import GroupStudent
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

def create(groupStudent:GroupStudent):
    sqlQuery = 'insert into group_students (groupid, studentusername) values(%s, %s);'
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
        cursor.execute(sqlQuery, (groupStudent.groupID, groupStudent.studentUsername))

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

def update(new:GroupStudent, groupStudent:GroupStudent):
    sqlQuery = 'update group_students set groupid=%s, studentusername = %s\
        where groupid=%s and studentusername=%s;'

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
            (groupStudent.groupID, groupStudent.studentUsername,
            new.groupID, new.studentUsername))

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

def readByUser(username:str)->Dict:
    sqlQuery = 'select groupid, studentusername \
        from group_students where studentusername=%s;'

    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )

        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sqlQuery, (username,))
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

def readByGroup(id:int)->Dict:
    sqlQuery = 'select  groupid, studentusername \
        from group_students where groupid=%s;'

    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )

        cursor = connection.cursor(cursor_factory=RealDictCursor)
        cursor.execute(sqlQuery, (id,))
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

def delete(groupID:int, studentUsername:str):
    sqlQuery = 'delete from group_students where studentusername=%s and groupid=%s;'

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
            (studentUsername, groupID))

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

def readStudentsIDbyGroup(groupID:int)->Dict:
    sqlQuery = 'select u.id, u.fullname from group_students gs\
    inner join users u on u.username = gs.studentusername \
    and gs.groupid = %s;'

    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )

        cursor = connection.cursor()
        cursor.execute(sqlQuery, (groupID,))
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