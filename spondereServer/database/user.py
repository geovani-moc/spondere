from entity.user import User
from database.database import getConnection
from passlib.context import CryptContext

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

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


# def getPassword_hash(password):
#     return pwd_context.hash(password)

def checkUser(data: User):
    connection = getConnection()
    cur = connection.cursor()
    sql_query = 'select username, password from users where username = %s'
    cur.execute(sql_query, (User.userName, ))
    
    for user in fake_users_db:
        if user.userName == data.userName and verifyPassword(user.password, data.password):
            return True
    return False


def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

