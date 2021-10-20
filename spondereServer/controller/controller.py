from fastapi import File, UploadFile, Depends
from fastapi.responses import HTMLResponse
from recognition.faceRecognition import verifyFace
from settings import EIGENFACES_NUMBER_COMPONENTS
from database import biometrics
from database.user import checkUser
from entity.user import User
from fastapi import FastAPI, Body
from entity.discipline import Discipline
from controller.security import signJWT, JWTBearer

app = FastAPI()

#antigo metodo de autenticação
#from fastapi.security import OAuth2PasswordBearer
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get('/robots.txt')
async def robotsTxt():
    content = 'User-agent: * Disallow: /'
    return HTMLResponse(content=content)

@app.get('/')
async def homePage():
    content = 'sponde API'
    return HTMLResponse(content = content)


@app.post("/user/signup", tags=["user"])
async def createUser(user:User = Body(...)):
    #users.append(user) 
    #verificar onde é necessario salvar os dados do usuario
    return signJWT(user.userName)


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
