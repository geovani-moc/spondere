from fastapi import (
    File, 
    UploadFile, 
    Depends,
    FastAPI,
    Body
    ) 
from fastapi.responses import HTMLResponse
from recognition.findFace import findFace
from database.user import checkUser
from entity.user import User, UserCredential
from entity.discipline import Discipline
from controller.security import signJWT, JWTBearer
from util.image import checkUploadedImage
from database import user as userDB
from recognition.faceRecognition import verifyFace
from entity.academicClass import AcademicClass

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


@app.post("/usuario/criar", tags=["Usuário"])
async def createUser(user:User = Body(...)):
    id, error = userDB.create(user)

    return {'User id':user.code, 'error': error}
    

@app.post("/login", tags=["Autenticação"])
async def userLogin(user: UserCredential):

    if checkUser(user.userName, user.password):
        return signJWT(user.userName)

    return {"invalid_access": "Usuário ou senha inválidos."}



#@app.post("/v1/checar_biometria", tags=["Biometria"])
@app.post("/v1/checar_biometria", dependencies=[Depends(JWTBearer())], tags=["Biometria"])
async def checkBiometry(userCode:str, file: UploadFile = File(...)):
    contents = await file.read()
    image = checkUploadedImage(contents)

    result:bool = False

    if image is None: return {"recognition": False,"error": "sem imagem"}

    face, error = findFace(image)
    
    if error is None:
        result = verifyFace(face, userCode)
        #salvar face(frequencia)
        if not result: return{"recognition": result, "error":"Face não definida."}

    return {"recognition": result, "error": None}

@app.post("/disciplinas", dependencies=[Depends(JWTBearer())], tags=["Disciplina"])
async def add_post(discipline: Discipline) -> dict:
       
    return {
        "result": "post added."
    }

@app.post("/aula/criar", dependencies=[Depends(JWTBearer())], tags=['Aula'])
async def create_AcademicClass(academicClass:AcademicClass) -> dict:

    return {
        "result": "class create."
    }

@app.post("/aula/editar", dependencies=[Depends(JWTBearer())], tags=['Aula'])
async def update_AcademicClass(academicClass:AcademicClass)-> dict:

    return{
        "result": "class updated."
    }

@app.post("/aula/apagar", dependencies=[Depends(JWTBearer())], tags=['Aula'])
async def delete_academicClass(codeAcademicClass:str) -> dict:
    
     return{
         "result": "class deleted."
     }

@app.post("/aula/obter", dependencies=[Depends(JWTBearer())], tags=['Aula'])
async def get_academicClass(codeStudent:str) -> dict:

    return {
        "result": "class caught."
    }

 