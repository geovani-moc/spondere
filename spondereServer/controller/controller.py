from fastapi import File, UploadFile, Depends
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from recognition.faceRecognition import verifyFace
from settings import EIGENFACES_NUMBER_COMPONENTS
from database import biometrics
from database.user import checkUser
from entity.user import User, UserCredential
from fastapi import FastAPI, Body
from entity.discipline import Discipline
from controller.security import signJWT, JWTBearer

app = FastAPI()


@app.get('/robots.txt')
async def robotsTxt():
    content = 'User-agent: * Disallow: /'
    return HTMLResponse(content=content)

@app.on_event("shutdown")
async def shutdown_event():
    print("Aplicação encerrada.")


@app.get('/')
async def homePage():
    content = 'sponde API<br>\
        docs<br>\
        redoc'
    return HTMLResponse(content = content)


@app.post("/user/signup", tags=["Usuário"])
async def createUser(user:User = Body(...)):
    #users.append(user) 
    #verificar onde é nescessario salvar os dados do usuario
    return signJWT(user.userName)


@app.post("/login", tags=["Autenticação"])
async def userLogin(user: UserCredential):

    if checkUser(user.userName, user.password):
        return signJWT(user.userName)

    return {"invalid_access": "Usuário ou senha inválidos."}


@app.post("/v1/checar_biometria", dependencies=[Depends(JWTBearer())], tags=["Biometria"])
async def checkBiometry(user: User, image: UploadFile = File(...)):
    trainedFeature, error = biometrics.read(user.code)
    if error is not None:
        return{"Error": error}

    result, error = verifyFace(trainedFeature, image, EIGENFACES_NUMBER_COMPONENTS)
    if error is not None:
        return{"Error": error}

    return {"Face": 'face pertence ao usuário.'}

@app.post("/disciplinas", dependencies=[Depends(JWTBearer())], tags=["Disciplina"])
async def add_post(discipline: Discipline) -> dict:
       
    return {
        "data": "post added."
    }
