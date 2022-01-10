from datetime import datetime
from pydantic.main import BaseModel
from typing import Optional

class Biometrics(BaseModel):
    id:int = None
    studentID:int = None
    createDate: Optional[datetime] = None
    deactivate:bool = None
    invalid:bool = None

    class Config:
        schema_extra = {
            "example":{
                "studentID": 1,
                "createDate": "2021, 11, 24, 15, 46, 59, 24384",
            }
        }
