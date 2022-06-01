from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from numpy import tile
from controller.user import router as userRouter
from controller.biometry import router as biometryRouter
from controller.discipline import router as disciplineRouter
from controller.academicClass import router as academicClassRouter
from controller.period import router as periodRouter
from controller.group import router as groupRouter
from controller.groupStudent import router as groupStudentRouter
from controller.groupProfessor import router as groupProfessorRouter
from controller.validation import router as validationRouter
from controller.frequency import router as frequencyRouter

tagsMetadata = [
    {
        "name":"Usuário",
        "description":"Gerenciamento de usuários",
    },
]

descriptionApp = "Sistema para controle de frequência acadêmica por meio de verificação biométrica"

app = FastAPI(
    openapi_tags=tagsMetadata,
    title="Spondere server",
    description=descriptionApp,
    version="0.9.0",
)

@app.get('/robots.txt')
async def robotsTxt():
    content = 'User-agent: * Disallow: /'
    return HTMLResponse(content=content)

@app.get('/')
async def homePage():
    content = '<center><h1>Sponde API</h1><br>\
        <a href="/docs">Docs</a><br>\
        <a href="/redoc">Redoc</a>\
        </center>'
    return HTMLResponse(content = content)

app.include_router(userRouter, tags=["Usuário"], prefix="/usuario")
app.include_router(biometryRouter, tags=["Biometria"], prefix="/biometria")
app.include_router(disciplineRouter, tags=["Disciplina"], prefix="/disciplina")
app.include_router(academicClassRouter, tags=["Aula"], prefix="/aula")
app.include_router(periodRouter, tags=["Período"], prefix="/periodo")
app.include_router(groupRouter, tags=["Grupo"], prefix="/grupo")
app.include_router(groupStudentRouter, tags=["Groupo de  discentes"], prefix="/grupoDiscentes")
app.include_router(groupProfessorRouter, tags=["Grupo de docentes"], prefix="/grupoDocentes")
app.include_router(validationRouter, tags=["Validação"], prefix="/validacao")
app.include_router(frequencyRouter, tags=["Frequência"], prefix="/frequencia")