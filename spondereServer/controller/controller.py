#https://panda.ime.usp.br/aulasPython/static/aulasPython/aula20.html
#https://fastapi.tiangolo.com/tutorial/request-files/?h=fil
#https://towardsdatascience.com/25x-times-faster-python-function-execution-in-a-few-lines-of-code-4c82bdd0f64c

#https://pydantic-docs.helpmanual.io/

from typing import Dict, Optional, List
from fastapi import File, UploadFile, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from recognition.faceRecognition import verifyFace
from settings import EIGENFACES_NUMBER_COMPONENTS, PATH_IMAGES
from util.image import saveBinaryImagesInDataset
from persistence import biometrics
from entity.user import User, UserLogin
from entity.discipline import Discipline
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import FastAPI, Body
import time

from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

users = []
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}
app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "002ba35be5e3daadcc1c97d634d5a496bf9524d9d7757eca3f3699f7b0f6b834"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def tokenResponse(token: str):
    return {
        "access_token": token
    }

def signJWT(user_id:str )->Dict[str, str]:
    accessInfo = {
        "user_id": user_id,
        "expires": time.time() + ACCESS_TOKEN_EXPIRE_MINUTES
    }
    token = jwt.encode(accessInfo, SECRET_KEY, algorithm=ALGORITHM)

    return tokenResponse(token)

def decodeJWT(token: str) -> dict:
    try:
        decodedToken = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decodedToken if decodedToken["expires"] >= time.time() else None
    except:
        return {}

@app.post("/user/signup", tags=["user"])
async def createUser(user: User = Body(...)):
    users.append(user) 
    return signJWT(user.email)

def checkUser(data: UserLogin):
    for user in users:
        if user.email == data.email and user.password == data.password:
            return True
    return False

@app.post("/user/login", tags=["user"])
async def user_login(user: UserLogin = Body(...)):
    if checkUser(user):
        return signJWT(user.email)
    return {
        "error": "Wrong login details!"
    }

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            accessInfo = decodeJWT(jwtoken)
        except:
            accessInfo = None
        if accessInfo:
            isTokenValid = True
        return isTokenValid

@app.post("/disciplinas", dependencies=[Depends(JWTBearer())], tags=["disciplines"])
async def add_post(discipline: Discipline) -> dict:
    discipline.code = len(disciplines) + 1
    disciplines.append(discipline.dict())
    return {
        "data": "post added."
    }

#--------------------------------------------------------------




def fake_hash_password(password: str):
    return "fakehashed" + password

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None

class UserInDB(User):
    hashed_password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = get_user(fake_users_db, token)
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user
    


#teste de autenticação
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]

#------------------------------------------------------------------------------
@app.post("/v1/enviar_imagens/")
async def uploadImages(user: User, files: List[UploadFile] = File(...)):
    
    images = []
    for file in files:
        images.append(file.file)

    error = saveBinaryImagesInDataset(images, PATH_IMAGES, user.code)
    if error is not None:
        return{"Imagem status": "Erro ao gravar imagens", 
        "ERROR": error}

    return {"Imagem status": "OK"}


@app.post("v1/checar_biometria")
async def checkBiometry(user: User, image: UploadFile = File(...)):
    trainedFeature, error = biometrics.read(user.code)
    if error is not None:
        return{"Error": error}

    result, error = verifyFace(trainedFeature, image, EIGENFACES_NUMBER_COMPONENTS)
    if error is not None:
        return{"Error": error}

    return {"Face": 'face pertence ao usuário.'}


@app.get("/")
async def main():
    content = """
<body>
<form action="/v1/imagens/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)

# @app.get("/v1/items/{item_id}")
# def read_item(item_id: int, q: Optional[str] = None):
#     return {"item_id": item_id, "q": q}


# @app.put("/v1/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}
