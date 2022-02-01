import logging
from entity.discipline import Discipline
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

def create(discipline: Discipline):
    sqlQuery = 'insert  into discipline (code, name, description)\
        values(%s, %s, %s) returning id;'
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
            (discipline.code, discipline.name, discipline.description))

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
    sqlQuery = 'select id, code, \"name\", description from discipline where id = %s;'
    discipline = Discipline()
    
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
        
        (discipline.id,
        discipline.code, 
        discipline.name, 
        discipline.description) = cursor.fetchone()

        connection.commit()

    except pg.OperationalError as e:
        logging.exception(e)
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return discipline

def update(id:int, discipline: Discipline):
    sqlQuery = 'UPDATE discipline SET semesterid = %s, \"name\" = %s, description = %s WHERE id = %s;'
    
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
            (discipline.semesterID, discipline.name, discipline.description, id))
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
    sqlQuery = 'delete from discipline where id = %s;'
    
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

def readActiveByProfessor(username:str):
    sqlQuery = 'select d.id, d.code, d.\"name\", d.description from "groups" g inner join\
    group_professors gp on gp.groupid = g.id and gp.professorusername = %s and g.active is true \
    inner join discipline d on d.id = g.disciplineid\
    inner join "period" p on g.semesterid = p.id and p.active is true;'
    
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