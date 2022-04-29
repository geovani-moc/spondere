from typing import Optional
from pydantic.main import BaseModel

class User(BaseModel):
    id:int = None
    username:str = None
    password: str = None
    email: Optional[str] = None
    fullName: str = None
    disabled: bool = None
    professor: bool = None
    student: bool = None
    administrator: bool = None

    class Config:
        schema_extra = {
            "example": {
                "username" : "geo",
                "password": "$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42",
                "email": "geo@facu.gov.br",
                "fullName": "Geovani Souza",
                "disabled": False,
                "professor": True,
                "student": False,
                "administrator": True
            }
        }

class UserCredential(BaseModel):
    username:str = None
    password: str = None

    class Config:
        schema_extra = {
            "example": {
                "username" : "user",
                "password": "123"
            }
        }
