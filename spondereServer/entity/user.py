from typing import List, Optional

from pydantic.main import BaseModel

class User(BaseModel):
    userName:str = None
    code: str = None
    faceFeatures: Optional[List[int]] = None
    # firstName: str = None
    # lastName: str = None
    password: str = None
    # status: int = None
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

    class Config:
        schema_extra = {
            "example": {
                "userName" : "usuario 1",
                "email": "user@user.com",
                "password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW"
            }
        }
