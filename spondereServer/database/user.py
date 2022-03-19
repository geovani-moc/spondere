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
from settings import(
    USER_TYPE_ADMIN,
    USER_TYPE_PROFESSOR,
    USER_TYPE_STUDENT
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
            (user.username, user.password, user.email, user.fullName,
            user.disabled, user.professor, user.student, user.administrator))
        id = cursor.fetchone()[0]

        connection.commit()

    except Exception as e:
        print(e)
        raise HTTPException(status_code=406,
                detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return id

def update(id:int, updatedUser: User):
    sqlQuery = 'UPDATE users SET username = %s, \"password\" = %s,\
    email = %s, fullname = %s, disabled = %s, professor = %s,\
    student = %s, administrator = %s  WHERE id = %s;'

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
            (updatedUser.username, updatedUser.password, updatedUser.email, updatedUser.fullName,
            updatedUser.disabled, updatedUser.professor, updatedUser.student, updatedUser.administrator, id))

        connection.commit()

    except:
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return None

def read(username: str):
    sqlQuery = 'select id, username, fullname, email, disabled, administrator, professor, student \
        from users where username = %s;'
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
        cursor.execute(sqlQuery, (username,))
        (user.id, user.username, user.fullName, user.email, user.disabled,
                user.administrator, user.professor, user.student) = cursor.fetchone()

    except:
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.")
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return user

def delete(username: str):
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
            (username,))

        connection.commit()

    except:
        raise HTTPException(status_code=406,
            detail="Erro de conexão com o banco de dados.") 
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return None

def checkUser(username: str, password:str):
    if username is None or password is None:
        return False, -1

    userType = -1
    user = User()
    sql_query = "select username, \"password\", professor, student, administrator from users where username = %s;"

    try:
        connection = pg.connect(
            user = DB_USERNAME,
            password = DB_PASSWORD,
            host = HOST,
            port = PORT,
            database = DB_NAME
        )

        cursor = connection.cursor()
        cursor.execute(sql_query, (username, ))
        (user.username, user.password, user.professor, 
        user.student, user.administrator) = cursor.fetchone()

    except:
        raise HTTPException(status_code=406,
            detail="u001") 
    finally:
        if (connection):
            cursor.close()
            connection.close()
    
    if user.administrator: userType = USER_TYPE_ADMIN
    elif user.professor: userType = USER_TYPE_PROFESSOR
    elif user.student: userType = USER_TYPE_STUDENT
    
    if user.username == username and verifyPassword(password, user.password):
       return True, userType

    return False, userType

def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
