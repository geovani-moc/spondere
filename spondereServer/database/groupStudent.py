import logging
from typing import List
from entity.groupStudent import GroupStudent
from fastapi import HTTPException
import psycopg2 as pg
from config import(
    DB_NAME,
    DB_PASSWORD,
    DB_USERNAME, 
    HOST,
    PORT
)

def create(groupStudent:GroupStudent):
    sqlQuery = 'insert into group_students  (groupid, studentusername) values(%s, %s);'
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

def readByUser(username:str):
    sqlQuery = 'select groupid, studentusername \
        from group_students where studentusername=%s;'
    groups:List[GroupStudent] = []

    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )

        cursor = connection.cursor()
        cursor.execute(sqlQuery, (username,))
        temp = cursor.fetchall()
        
        for (groupID, student) in temp:

            temp = GroupStudent()
            temp.groupID = groupID
            temp.studentUsername = student
                        
            groups.append(temp)
        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.")
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return groups

def readByGroup(id:int):
    sqlQuery = 'select  groupid, studentusername \
        from group_students where groupid=%s;'
    students:List[GroupStudent] = []

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
        temp = cursor.fetchall()
        
        for (groupID, student) in temp:

            temp = GroupStudent()
            temp.groupID = groupID
            temp.studentUsername = student
                        
            students.append(temp)
        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.")
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return students


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