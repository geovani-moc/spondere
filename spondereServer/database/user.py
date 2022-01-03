from entity.user import User
from passlib.context import CryptContext
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

    sqlQuery = 'insert  into users (username, code, "password", status,\
     email, fullname, disabled) values (%s, %s, %s, %s, %s, %s, %s);'

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
        (   user.userName,
            user.code,
            user.password,
            user.status,
            user.email,
            user.fullName,
            user.disabled,
        ))
        connection.commit()

    except (Exception, pg.DatabaseError) as error:
        return "Erro de conexão com o banco de dados: " + error
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return None

def update(user: User):
    return None

def read(code: str):
    sqlQuery = 'select code, userName, fullname, email, disabled, password, status\
        from users where code = %s;'
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
        cursor.execute(sqlQuery, (code,))
        (user.code, user.userName, user.fullName, user.email, user.disabled,\
                user.password, user.status) = cursor.fetchone()

        connection.commit()

    except (Exception, pg.DatabaseError) as error:
        print("Erro de conexão com o banco de dados: " + error)
    finally:
        if (connection):
            cursor.close()
            connection.close()

    return user, error

def delete(code: str):
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

    except (Exception, pg.DatabaseError) as error:
        print("Erro de conexão com o banco de dados: ", error)
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
    sqlQuery = 'select code, username, fullName, email, disabled, password, status\
        from users where code = %s;'
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
        cursor.execute(sqlQuery, ('gpds',))
        (user.code, user.userName, user.fullName, user.email, user.disabled,\
                user.password, user.status) = cursor.fetchone()

        connection.commit()

    except (Exception, pg.DatabaseError) as error:
        print("Erro de conexão com o banco de dados: " + error)
    finally:
        if (connection):
            cursor.close()
            connection.close()
    print(user)