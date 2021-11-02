from fastapi import (
    File, 
    UploadFile, 
    Depends,
    FastAPI,
    Body
    ) 
from fastapi.responses import HTMLResponse
from recognition.faceRecognition import faceRecognition
from database.user import checkUser
from entity.user import User, UserCredential
from entity.discipline import Discipline
from controller.security import signJWT, JWTBearer
from util.image import checkUploadedImage

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


@app.post("/v1/checar_biometria", tags=["Biometria"])
#@app.post("/v1/checar_biometria", dependencies=[Depends(JWTBearer())], tags=["Biometria"])
async def checkBiometry(file: UploadFile = File(...)):
    contents = await file.read()
    image = checkUploadedImage(contents)

    result:bool
    error:str

    if image is None:
        error = "Sem imagem"
        result = False
        return {
            "recognition": result,
            "error": error
        }
    else:
        error = None
        result = True

    #result, error = faceRecognition(user.code, image)
    if error is not None:
        return {
            "recognition": False,
            "error": error
        }   

    if not result:
        return{
            "recognition": result,
            "error":"Face não definida."
        }

    return {
        "recognition": result,
        "error": None}

@app.post("/disciplinas", dependencies=[Depends(JWTBearer())], tags=["Disciplina"])
async def add_post(discipline: Discipline) -> dict:
       
    return {
        "data": "post added."
    }
