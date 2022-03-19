from fastapi import (
    APIRouter, 
    Depends,
    Request, 
    HTTPException)
from controller.security import (
    JWTBearer,
    getCurrentUserName,
    getCurrentUserType,
    signJWT)
from database import user as userDB
from entity.user import User, UserCredential
from database.user import checkUser
from settings import(
    USER_TYPE_ADMIN,
    USER_TYPE_PROFESSOR,
    USER_TYPE_STUDENT
)


router = APIRouter()

@router.post("", dependencies=[Depends(JWTBearer())])
async def createUser(request:Request, newUser:User):
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)
    user = userDB.read(username)

    if not user.administrator:
        return {'detail': 'u002'}
    
    id = userDB.create(newUser)
    return {'id': id}
    
@router.post("/login")
async def userLogin(userCredential: UserCredential):
    result, userType = checkUser(userCredential.username, userCredential.password)

    if result:
        return signJWT(userCredential.username, userType)

    raise HTTPException(status_code=406,
            detail="u001") 

@router.get("", dependencies=[Depends(JWTBearer())])
async def getCurrentUser(request:Request):
    authorization = request.headers.get("authorization")
    username = getCurrentUserName(authorization)

    currentUser = userDB.read(username)
    return {'user': currentUser}

@router.put("/{id}", dependencies=[Depends(JWTBearer())])
async def updatePeriod(id:int, newUser:User, request:Request):
    authorization = request.headers.get("authorization")
    userType = getCurrentUserType(authorization)

    if userType != USER_TYPE_ADMIN:
        raise HTTPException(status_code=401,
            detail="O usuário não tem privilegio de administrador.")
    
    userDB.update(id, newUser)
    return {
        "result": "success"
    }