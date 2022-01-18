from fastapi import (
    APIRouter, 
    Depends,
    Body,
    Request)
from controller.security import (
    JWTBearer,
    getCurrentUserName,
    signJWT)
from database import user as userDB
from entity.user import User, UserCredential
from database.user import checkUser


router = APIRouter()

@router.post("", dependencies=[Depends(JWTBearer())])
async def createUser(request:Request, user:User = Body(...)):
    authorization = request.headers.get("authorization")
    userName = getCurrentUserName(authorization)
    user = userDB.read(userName)

    if not user.administrator:
        return {'User code': None, 'error': 'u002'}
    
    id = userDB.create(user)
    return {'User code': id, 'error':None}
    
@router.post("/login")
async def userLogin(user: UserCredential):

    if checkUser(user.userName, user.password):
        return signJWT(user.userName)

    return {"invalid_access": "Usuário ou senha inválidos."}

@router.get("", dependencies=[Depends(JWTBearer())])
async def getCurrentUser(request:Request):
    authorization = request.headers.get("authorization")
    userName = getCurrentUserName(authorization)

    currentUser = userDB.read(userName)
    return {'user': currentUser}
