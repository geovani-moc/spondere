from datetime import datetime
from typing import List

from pydantic.main import BaseModel

class Frequency(BaseModel):
    studentCode: str = None
    academicClassCode: str = None
    method:int = None
    createDate: datetime = None
    geolocalization: str = None
    validationType: int = None
    photo:List[int] = None#mudar para binário

    class Config:
        schema_extra = {
            "example": {
                "studentCode" : "fdkn3",
                "academmicClassCode": "434mnd",
                "method": 1,
                "createDate": "12/12/1999",
                "geolocalization": "72.32323, 23.43438",
                "validationType": 2
            }
        }