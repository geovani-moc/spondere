from entity.discipline import Discipline
from fastapi import HTTPException
import psycopg2 as pg
from config import(
    DB_NAME,
    DB_PASSWORD,
    DB_USERNAME, 
    HOST,
    PORT
)

def create(discipline: Discipline):
    sqlQuery = 'insert  into discipline (semesterid, name, description)\
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
            (discipline.semesterID, discipline.name, discipline.description))

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

def read(id:int):
    sqlQuery = 'select id, semesterid, \"name\", description from discipline where id = %s;'
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
        discipline.semesterID, 
        discipline.name, 
        discipline.description) = cursor.fetchone()

        connection.commit()

    except:
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

    except:
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return discipline


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

    except:
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return None