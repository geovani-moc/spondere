
from typing import List
from datetime import datetime
from pydantic.main import BaseModel

#pesquisar sobre o Optional da biblioteca typing
class Biometrics(BaseModel):
    code: str = None
    feature: List[int] = None
    createDate: datetime = None
    status: int = None
    studentCode: str = None

    class Config:
        schema_extra = {
            "example":{
                "code": "fdkj8",
                "createDate": "21/12/1992",
                "status": 1,
                "studentCode": "jhfd2"
            }
        }
