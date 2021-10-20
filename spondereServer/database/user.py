from logging import error
from time import process_time

from passlib.utils import repeat_string
from entity.user import User
from database.database import postgresSQL
from passlib.context import CryptContext
from psycopg2 import DatabaseError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create(user: User):
    return None

def update(user: User):
    return None

def read(code: str):
    user: User
    return user

def delete(code: str):
    return None


# def getPassword_hash(password):
#     return pwd_context.hash(password)

def checkUser(data: User):
    if data.userName is None or data.password is None:
        return False

    user:User
    sql_query = 'select username, password from users where username = %s'

    try:
        connection = postgresSQL.getconn()

        if(connection):
            cur = connection.cursor()
            cur.execute(sql_query, (data.userName, ))
            user.userName, user.password = cur.fetchone()

            postgresSQL.putconn(connection)

    except (Exception, DatabaseError) as error:
        print("Erro de conexão com o banco de dados: ", error)
    
    if user.userName == data.userName and verifyPassword(user.password, data.password):
        return True

    return False


def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

