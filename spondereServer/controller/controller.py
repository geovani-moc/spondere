from fastapi import (
    File, 
    UploadFile, 
    Depends,
    FastAPI,
    Body,
    HTTPException
    ) 
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from recognition.findFace import findFace
from database.user import checkUser
from entity.user import User, UserCredential
from entity.discipline import Discipline
from controller.security import getCurrentUserName, signJWT, JWTBearer
from util.image import checkUploadedImage
from database import user as userDB
from database import discipline as disciplineDB
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
    content = '<center><h1>Sponde API</h1><br>\
        <a href="/docs">Docs</a><br>\
        <a href="/redoc">Redoc</a>\
        </center>'
    return HTMLResponse(content = content)
 
@app.post("/usuario/criar", tags=["Usuário"])
async def createUser(request:Request, user:User = Body(...)):
    authorization = request.headers.get("authorization")
    userName = getCurrentUserName(authorization)

    user = userDB.read(userName)

    if not user.administrator:
        return {'User code':-1, 'error': 'u002'}
    
    code, error = userDB.create(user)

    return {'User code':user.code, 'error': error}
    
@app.get("/login", tags=["Usuário"])
async def userLogin(user: UserCredential):

    if checkUser(user.userName, user.password):
        return signJWT(user.userName)

    return {"invalid_access": "Usuário ou senha inválidos."}

@app.post("/v1/checar_biometria", dependencies=[Depends(JWTBearer())], tags=["Biometria"])
async def checkBiometry(request:Request, file: UploadFile = File(...)):
    authorization = request.headers.get("authorization")
    userName = getCurrentUserName(authorization)

    contents = await file.read()
    image = checkUploadedImage(contents)

    result:bool = False

    if image is None: return {"recognition": False,"error": "sem imagem"}

    face, error = findFace(image)
    
    if error is None:
        result = verifyFace(face, userName)
        #salvar face(frequencia)
        if not result: return{"recognition": result, "error":"Face não definida."}

    return {"recognition": result, "error": None}

@app.get("/disciplinas", dependencies=[Depends(JWTBearer())], tags=["Disciplina"])
async def readAllDisciplines(request:Request) -> dict:
    authorization = request.headers.get("authorization")
    userName = getCurrentUserName(authorization)
    disciplines = disciplineDB.read(userName=userName)

    return {
        "discipline": disciplines
    }

@app.get("/disciplinas/{id}", dependencies=[Depends(JWTBearer())], tags=["Disciplina"])
async def readDiscipline(id:int ,request:Request):
    authorization = request.headers.get("authorization")
    userName = getCurrentUserName(authorization)
    specificDiscipline = disciplineDB.read(userName=userName, id=id)
    return {
        "discipline": specificDiscipline
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