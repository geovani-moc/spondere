from calendar import TUESDAY
from os import truncate
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

def checkUser(userName: str, password:str):
    if userName is None or password is None:
        return False

    user = User()
    sql_query = "select username, \"password\" from users where username = %s;"

    try:
        connection = postgresSQL.getconn()

        if(connection):
            user.userName = "teste"
            cur = connection.cursor()
            cur.execute(sql_query, (userName, ))
            (user.userName, user.password) = cur.fetchone()

            postgresSQL.putconn(connection)

    except (Exception, DatabaseError) as error:
        print("Erro de conexão com o banco de dados: ", error)
    
    if user.userName == userName and verifyPassword(password, user.password):
       return True

    return False


def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

