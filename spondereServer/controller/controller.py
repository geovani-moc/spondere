from logging import currentframe
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
 
@app.post("/usuario", tags=["Usuário"])
async def createUser(request:Request, user:User = Body(...)):
    authorization = request.headers.get("authorization")
    userName = getCurrentUserName(authorization)

    user = userDB.read(userName)

    if not user.administrator:
        return {'User code': None, 'error': 'u002'}
    
    id = userDB.create(user)

    return {'User code': id, 'error':None}
    
@app.post("/login", tags=["Usuário"])
async def userLogin(user: UserCredential):

    if checkUser(user.userName, user.password):
        return signJWT(user.userName)

    return {"invalid_access": "Usuário ou senha inválidos."}

@app.get("/usuario", dependencies=[Depends(JWTBearer())], tags=["Usuário"])
async def getCurrentUser(request:Request):
    authorization = request.headers.get("authorization")
    userName = getCurrentUserName(authorization)

    currentUser = userDB.read(userName)
    return {'user': currentUser}


@app.post("/checar_biometria", dependencies=[Depends(JWTBearer())], tags=["Biometria"])
async def checkBiometry(request:Request, file: UploadFile = File(...)):
    authorization = request.headers.get("authorization")
    userName = getCurrentUserName(authorization)

    contents = await file.read()
    image = checkUploadedImage(contents)

    result:bool = False

    if image is None: return {"recognition": False,"error": "sem imagem"}

    face, error = findFace(image)
    if error:
        raise HTTPException(status_code=500,
            detail="Erro no sistema de reconhecimento facial: \n" + error) 
    
    if error is None:
        result = verifyFace(face, userName)
        #salvar face(frequencia) --await
        if not result: return{"recognition": result, "error":"Face não definida."}

    return {"recognition": result, "error": None}

@app.get("/disciplinas/{id}", dependencies=[Depends(JWTBearer())], tags=["Disciplina"])
async def readDiscipline(id:int):
    discipline = disciplineDB.read(id=id)
    return {
        "discipline": discipline
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