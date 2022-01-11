from entity.user import User
from passlib.context import CryptContext
from fastapi import HTTPException
import psycopg2 as pg
from config import(
    DB_NAME,
    DB_PASSWORD,
    DB_USERNAME, 
    HOST,
    PORT
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create(user: User):
    sqlQuery = 'insert  into users (username, \"password\", email, fullname,\
        disabled, professor, student, administrator) values (%s, %s, %s, %s, %s, %s, %s, %s) returning id;'
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
            (user.userName, user.password, user.email, user.fullName,
            user.disabled, user.professor, user.student, user.administrator))
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

def update(userName:str, updatedUser: User):
    sqlQuery = 'UPDATE users SET username = %s, /"password/" = %s,\
    email = %s, fullname = %s, disabled = %s, professor = %s,\
    student = %s, administrator = %s  WHERE username = %s;'

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
            (updatedUser.userName, updatedUser.password, updatedUser.email, updatedUser.fullName,
            updatedUser.disabled, updatedUser.professor, updatedUser.student, updatedUser.administrator, userName))

        connection.commit()

    except:
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return None

def read(userName: str):
    sqlQuery = 'select id, username, fullname, email, disabled, administrator, professor, student \
        from users where username = %s;'
    error = None
    user = User()
    
    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )


        cursor = connection.cursor()
        cursor.execute(sqlQuery, (userName,))
        (user.id, user.userName, user.fullName, user.email, user.disabled,
                user.administrator, user.professor, user.student) = cursor.fetchone()

        connection.commit()

    except:
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.")
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return user, error

def delete(userName: str):
    sqlQuery = 'delete from users where username = %s;'

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
            (userName,))

        connection.commit()

    except:
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return None

def checkUser(userName: str, password:str):
    if userName is None or password is None:
        return False

    user = User()
    sql_query = "select username, \"password\" from users where username = %s;"

    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )

        cursor = connection.cursor()
        cursor.execute(sql_query, (userName, ))
        (user.userName, user.password) = cursor.fetchone()

    except:
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()
    
    if user.userName == userName and verifyPassword(password, user.password):
       return True

    return False

def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


if __name__ == '__main__':
    pass