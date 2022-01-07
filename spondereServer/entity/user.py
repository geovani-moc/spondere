from typing import List, Optional

from pydantic.main import BaseModel

class User(BaseModel):
    userName:str = None
    code: str = None
    password: str = None
    status: int = None
    email: Optional[str] = None
    fullName: str = None
    disabled: bool = None
    professor: bool = None
    student: bool = None
    administrator: bool = None

    class Config:
        schema_extra = {
            "example": {
                "userName" : "geo",
                "code": "gpds",
                "email": "user@user.com",
                "password": "$2a$12$XeC9hXg2D4PHXPaVyGy5FuNjU9SqblGpN073r./4NIiYXzdyZey42",
                "status": 1,
                "fullName": "Alcarmo da silva alves",
                "disabled": False,
                "administrator": True,
                "student": True
            }
        }

class UserCredential(BaseModel):
    userName:str = None
    password: str = None

    class Config:
        schema_extra = {
            "example": {
                "userName" : "geo",
                "password": "123"
            }
        }
