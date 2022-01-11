from entity.period import Period
import psycopg2 as pg
from config import(
    DB_NAME,
    DB_PASSWORD,
    DB_USERNAME, 
    HOST,
    PORT
)

def create(period:Period):
    sqlQuery = ''

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
            ())

        connection.commit()

    except (Exception, pg.DatabaseError) as error:
        return "Erro de conexão com o banco de dados: " + error
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return None

def read(id:int):
    sqlQuery = ''
    error = None
    discipline = Period()
    
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

    except (Exception, pg.DatabaseError) as error:
        print("Erro de conexão com o banco de dados: " + error)
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return discipline


def update(updatedPeriod: Period):
    return None


def delete(id:int ):
    return None