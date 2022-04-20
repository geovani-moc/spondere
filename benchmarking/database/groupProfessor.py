import logging
from typing import Dict, List

from sklearn.feature_extraction import DictVectorizer
from entity.groupProfessor import GroupProfessor
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

def create(groupProfessor:GroupProfessor):
    sqlQuery = 'insert into group_professors (groupid, professorusername) values(%s, %s);'
    
    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )
        cursor = connection.cursor()
        cursor.execute(sqlQuery, (groupProfessor.groupID, groupProfessor.professorUsername))

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

def update(new:GroupProfessor, groupProfessor:GroupProfessor):
    sqlQuery = 'update group_professors set groupid=%s, professorusername = %s\
        where groupid=%s and professorusername=%s;'

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
            (groupProfessor.groupID, groupProfessor.professorUsername,
            new.groupID, new.professorUsername))

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

def readByUser(username:str) -> Dict:
    sqlQuery = 'select groupid, professorusername \
        from group_professors where professorusername=%s;'

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

def readByGroup(id:int) -> Dict:
    sqlQuery = 'select  groupid, professorusername \
        from group_professors where groupid=%s;'

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


def delete(groupID:int, professorUsername:str):
    sqlQuery = 'delete from group_professors where professorusername=%s and groupid=%s;'

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
            (professorUsername, groupID))

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