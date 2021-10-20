import time
from jose import jwt
from typing import Dict
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException

SECRET_KEY = "002ba35be5e3daadcc1c97d634d5a496bf9524d9d7757eca3f3699f7b0f6b834"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Esquema de autenticação invalida.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Token invalido ou expirado.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Codigo de validação inválido.")

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
        "access_token": token
    }

def signJWT(user_id:str )->Dict[str, str]:
    accessInfo = {
        "user_id": user_id,
        "expires": time.time() + ACCESS_TOKEN_EXPIRE_MINUTES
    }
    token = jwt.encode(accessInfo, SECRET_KEY, algorithm=ALGORITHM)

    return tokenResponse(token)

def decodeJWT(token: str) -> dict:
    try:
        decodedToken = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return decodedToken if decodedToken["expires"] >= time.time() else None
    except:
        return {}