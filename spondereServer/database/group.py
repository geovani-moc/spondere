from entity.group import Group
from fastapi import HTTPException
import psycopg2 as pg
from config import(
    DB_NAME,
    DB_PASSWORD,
    DB_USERNAME, 
    HOST,
    PORT
)

def create(group: Group):
    sqlQuery = 'insert  into /"groups/" (code, begindate, enddate, disciplineid) values (%s, %s, %s, %s) returning id;'
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
            (group.code, group.beginDate, group.endDate, group.disciplineID))
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

def update(id:int, group:Group):
    sqlQuery = 'update  /"groups/" set code = %s, begindate = %s, enddate = %s,\
    deactivate = %s, disciplineid = %s where id = %s;'

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
            (group.code, group.beginDate, group.endDate,
             group.deactivate, group.disciplineID, id))

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
    sqlQuery = 'select id, code, begindate, enddate, deactivate , \
        disciplineid from /"groups/" where id = %s;'
    group = Group()
    
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
        (group.id, 
        group.code, 
        group.beginDate, 
        group.endDate, 
        group.deactivate, 
        group.disciplineID) = cursor.fetchone()

        connection.commit()

    except:
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.")
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return group

def delete(id:int):
    sqlQuery = 'delete from /"groups/" where id = %s;'

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