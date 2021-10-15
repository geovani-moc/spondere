from typing import List, Optional

from pydantic.main import BaseModel

class User(BaseModel):
    userName:str = None
    code: str = None
    #faceFeatures: Optional[List[int]] = None
    password: str = None
    status: int = None
    email: Optional[str] = None
    fullName: str = None
    disabled: bool = None

    class Config:
        schema_extra = {
            "example": {
                "userName" : "usuario 1",
                "code": "8aa100",
                "email": "user@user.com",
                "password": "356a192b7913b04c54574d18c28d46e6395428ab",
                "status": 1,
                "fullName": "Alcarmo da silva alves",
                "disabled": False
            }
        }
