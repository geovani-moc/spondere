from datetime import datetime
from typing import List
from typing import Optional
from pydantic.main import BaseModel

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Frequency(BaseModel):
    studentUsername: str = None
    academicClassID: int = None
    attendanceMethod:int = None
    createDate: datetime = None
    geolocalization: Optional[Point] = None
    validationType: int = None
    photo:List[bytes] = None

    class Config:
        schema_extra = {
            "example": {
                "studentUsername" : "geo",
                "academmicClassId": 1,
                "attendanceMethod": 1,
                "createDate": "12/12/1999",
                "validationType": 2
            }
        }