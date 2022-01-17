from sys import prefix
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from controller.user import router as userRouter
from controller.biometry import router as biometryRouter
from controller.discipline import router as disciplineRouter
from controller.academicClass import router as academicClassRouter
from controller.period import router as periodRouter
from controller.group import router as groupRouter
from database import period

app = FastAPI()

@app.get('/robots.txt')
async def robotsTxt():
    content = 'User-agent: * Disallow: /'
    return HTMLResponse(content=content)

# @app.on_event("shutdown")
# async def shutdown_event():
#     print("Aplicação encerrada.")

@app.get('/')
async def homePage():
    content = '<center><h1>Sponde API</h1><br>\
        <a href="/docs">Docs</a><br>\
        <a href="/redoc">Redoc</a>\
        </center>'
    return HTMLResponse(content = content)

app.include_router(userRouter, tags=["Usuário"], prefix="/usuario")
app.include_router(biometryRouter, tags=["Biometria"], prefix="/biometria")
app.include_router(disciplineRouter, tags=["disciplina"], prefix="/disciplina")
app.include_router(academicClassRouter, tags=["aula"], prefix="/aula")
app.include_router(periodRouter, tags=["Periodo"], prefix="/periodo")
app.include_router(groupRouter, tags=["grupo"], prefix="/grupo")