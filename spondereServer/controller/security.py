import time
from jose import jwt
from typing import Dict
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException
from config import(
    SECRET_KEY
)

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 864000 #10 dias em segundos

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = \
            await super(JWTBearer, self).__call__(request)
            
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403,
                detail="Esquema de autenticação invalida.")

            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, 
                detail="Token invalido ou expirado.")

            return credentials.credentials
        else:
            raise HTTPException(status_code=403, 
            detail="Codigo de validação inválido.")

    def verify_jwt(self, jwtoken: str) -> bool:
        isTokenValid: bool = False

        try:
            accessInfo = decodeJWT(jwtoken)
        except:
            accessInfo = None

        if accessInfo:
            isTokenValid = True

        return isTokenValid


def tokenResponse(token: str):
    return {
        "token": token
    }

def signJWT(username:str, userType:int )->Dict[str, str]:
    
    accessInfo = {
        "username": username,
        "expires": time.time() + ACCESS_TOKEN_EXPIRE_SECONDS,
        "user_type": userType
    }
    token = jwt.encode(accessInfo, SECRET_KEY, algorithm=ALGORITHM)

    return tokenResponse(token)

def decodeJWT(token: str) -> dict:
    try:
        decodedToken = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        if decodedToken["expires"] >= time.time():
            return decodedToken

    except:
        return {}

    return None

def getCurrentUserName(authorization:str) -> str:
    try:
        bearer, _, token =  authorization.partition(' ')
    
        if bearer != 'Bearer': 
            raise HTTPException(status_code=403,
                detail="Esquema de autenticação invalida.")   
        decodedToken = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if decodedToken.get("username") is None:
            raise HTTPException(status_code=500,
                detail="Usuário não identificado pelo token.")
        
    except:
        raise HTTPException(status_code=403,
                detail="Token inválido.")
    
    return decodedToken["username"]

def getCurrentUserType(authorization:str)->int:
    try:
        bearer, _, token =  authorization.partition(' ')
    
        if bearer != 'Bearer': 
            raise HTTPException(status_code=403,
                detail="Esquema de autenticação invalida.")   
        decodedToken = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        if decodedToken.get("user_type") is None:
            raise HTTPException(status_code=500,
                detail="Tipo de usuário não identificado pelo token.")
        
    except:
        raise HTTPException(status_code=403,
                detail="Token inválido.")
    
    return decodedToken["user_type"]
