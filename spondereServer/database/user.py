from entity.user import User
from database.database import postgresSQL
from passlib.context import CryptContext
from psycopg2 import DatabaseError

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create(user: User):

    sqlQuery = 'insert  into users (username, code, "password", status,\
     email, fullname, disabled) values (%s, %s, %s, %s, %s, %s, %s);'

    try:
        connection = postgresSQL.getconn()

        if(connection):
            cur = connection.cursor()
            cur.execute(sqlQuery, 
            (   user.userName,
                user.code,
                user.password,
                user.status,
                user.email,
                user.fullName,
                user.disabled,
             ))

            connection.commit()
            postgresSQL.putconn(connection)

    except (Exception, DatabaseError) as error:
        return "Erro de conexão com o banco de dados: " + error

    return None

def update(user: User):
    return None

def read(code: str):
    sqlQuery = 'select code, userName, fullname, email, disabled, password, status\
        from users where id = %s;'
    error = None
    user = User()
    
    try:
        connection = postgresSQL.getconn()

        if(connection):
            cur = connection.cursor()
            cur.execute(sqlQuery, (code,))
            (user.code, user.userName, user.fullName, user.email, user.disabled,\
                 user.password, user.status) = cur.fetchone()

            connection.commit()
            postgresSQL.putconn(connection)

    except (Exception, DatabaseError) as error:
        return -1, "Erro de conexão com o banco de dados: " + error

    return user, error

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

