from typing import ContextManager
import psycopg2
from psycopg2 import pool
from config import(
    MIN_CONNECTIONS,
    MAX_CONNECTIONS,
    DB_NAME,
    DB_PASSWORD,
    DB_USERNAME, 
    HOST,
    PORT
)

postgresSQL = psycopg2.pool.ThreadedConnectionPool(
        MIN_CONNECTIONS,
        MAX_CONNECTIONS,
        user = DB_USERNAME,
        password = DB_PASSWORD,
        host = HOST,
        port = PORT,
        database=DB_NAME
    )
if not postgresSQL:
    print("Erro ao tentar se conectar ao BD postgresSQL.")


@ContextManager
def getConnection():
    connection = postgresSQL.getconn()
    try:
        yield connection
    finally:
        postgresSQL.putconn(connection)
