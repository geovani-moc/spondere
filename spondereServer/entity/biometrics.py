from pydantic.main import BaseModel
from typing import Optional

class Biometrics(BaseModel):
    id:int = None
    studentID:int = None
    createDate: str = None
    active:bool = None
    invalid:bool = None
    failure:Optional[str] = None

    class Config:
        schema_extra = {
            "example":{
                "studentID": 1,
                "createDate": "2022-10-19 10:23:54+2",
                "active": True,
                "invalid": False
            }
        }
