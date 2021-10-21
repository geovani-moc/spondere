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


@app.get('/robots.txt')
async def robotsTxt():
    content = 'User-agent: * Disallow: /'
    return HTMLResponse(content=content)

@app.get('/')
async def homePage():
    content = 'sponde API<br> docs<br> redoc'
    return HTMLResponse(content = content)


@app.post("/user/signup", tags=["user"])
async def createUser(user:User = Body(...)):
    #users.append(user) 
    #verificar onde é necessario salvar os dados do usuario
    return signJWT(user.userName)


@app.post("/user/login", tags=["user"])
async def user_login(userName:str, password:str):
    if checkUser(userName, password):
        return signJWT(userName)

    return {"error": "Usuário ou senha inválidos."}


@app.post("/v1/checar_biometria", dependencies=[Depends(JWTBearer())], tags=["disciplines"])
async def checkBiometry(user: User, image: UploadFile = File(...)):
    trainedFeature, error = biometrics.read(user.code)
    if error is not None:
        return{"Error": error}

    result, error = verifyFace(trainedFeature, image, EIGENFACES_NUMBER_COMPONENTS)
    if error is not None:
        return{"Error": error}

    return {"Face": 'face pertence ao usuário.'}

@app.post("/disciplinas", dependencies=[Depends(JWTBearer())])
async def add_post(discipline: Discipline) -> dict:
       
    return {
        "data": "post added."
    }
