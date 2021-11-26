from typing import List
from datetime import datetime
from pydantic.main import BaseModel

class Biometrics(BaseModel):
    studentCode: str = None
    createDate: datetime = None
    status: int = None

    class Config:
        schema_extra = {
            "example":{
                "code": "fdkj8",
                "createDate": "2021, 11, 24, 15, 46, 59, 24384",
                "status": 1,
                "studentCode": "jhfd2"
            }
        }
