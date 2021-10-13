from typing import Dict
from fastapi import File, UploadFile, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordBearer
from recognition.faceRecognition import verifyFace
from settings import EIGENFACES_NUMBER_COMPONENTS
from persistence import biometrics
from entity.user import User
from passlib.context import CryptContext
from jose import jwt
from fastapi import FastAPI, Body
import time
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from entity.discipline import Discipline

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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Esquema de autenticação invalida.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Token invalido ou expirado.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Codigo de validação inválido.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            accessInfo = decodeJWT(jwtoken)
        except:
            accessInfo = None
        if accessInfo:
            isTokenValid = True
        return isTokenValid

@app.get('/robots.txt')
async def robotsTxt():
    content = 'User-agent: * Disallow: /'
    return HTMLResponse(content=content)

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
async def createUser(user:User = Body(...)):
    #users.append(user) 
    #verificar onde é necessario salvar os dados do usuario
    return signJWT(user.userName)


def verifyPassword(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# def getPassword_hash(password):
#     return pwd_context.hash(password)

def checkUser(data: User):
    #carregar os usuarios do banco de dados
    users = []
    for user in users:
        if user.userName == data.userName and verifyPassword(user.password, data.password):
            return True
    return False

@app.post("/user/login", tags=["user"])
async def user_login(user: User = Body(...)):
    if checkUser(user):
        return signJWT(user.userName)
    return {
        "error": "Usuário ou senha inválidos."
    }


@app.post("/v1/checar_biometria", dependencies=[Depends(JWTBearer())], tags=["disciplines"])
async def checkBiometry(user: User, image: UploadFile = File(...)):
    trainedFeature, error = biometrics.read(user.code)
    if error is not None:
        return{"Error": error}

    result, error = verifyFace(trainedFeature, image, EIGENFACES_NUMBER_COMPONENTS)
    if error is not None:
        return{"Error": error}

    return {"Face": 'face pertence ao usuário.'}

@app.post("/disciplinas", dependencies=[Depends(JWTBearer())], tags=["disciplines"])
async def add_post(discipline: Discipline) -> dict:
    discipline.code = len(disciplines) + 1
    disciplines.append(discipline.dict())
    return {
        "data": "post added."
    }
