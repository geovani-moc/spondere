import psycopg2
from config import(
    MIN_CONNECTIONS,
    MAX_CONNECTIONS,
    DB_NAME,
    DB_PASSWORD,
    DB_USERNAME, 
    HOST,
    PORT
)

try:
    postgresSQL = psycopg2.pool.ThreadedConnectionPool(
            MIN_CONNECTIONS,
            MAX_CONNECTIONS,
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database=DB_NAME
        )
except:
    print("Não foi possivel se conectar ao servidor.")
    postgresSQL = None

def newConnection():
    try:
        postgresSQL = psycopg2.pool.ThreadedConnectionPool(
            MIN_CONNECTIONS,
            MAX_CONNECTIONS,
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database=DB_NAME
        )
    except:
        postgresSQL = None
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