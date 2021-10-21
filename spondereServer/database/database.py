from typing import ContextManager
import psycopg2
from psycopg2 import connect, pool
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

# @ContextManager
# def getConnection():
#     connection = postgresSQL.getconn()
#     try:
#         yield connection
#     finally:
#         postgresSQL.putconn(connection)

# def getConnectio():
#     if postgresSQL:
#         return postgresSQL.getconn(), None
#     else:
#         return None, "Erro ao estabelece conexão pool."

def newConnection():
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
        return ("Erro ao tentar se conectar ao BD postgresSQL.")
    
    return None

if __name__ == "__main__":
    if postgresSQL:
        conn = postgresSQL.getconn()
        cur = conn.cursor()
        cur.execute("select username, \"password\" from users;")
        userName, password = cur.fetchone()
        postgresSQL.putconn(conn)

        print(userName, password)