from datetime import datetime
from typing import List
from typing import Optional
from pydantic.main import BaseModel

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Frequency(BaseModel):
    id:int = None
    studentID:int = None
    academicClassID: int = None
    ManualAttendance:bool = None
    BLEAttendance:bool = None
    QrCodeAttendance:bool = None
    createDate: datetime = None
    validationCode:str = None
    geolocalization: Optional[Point] = None
    photo:List[bytes] = None

    class Config:
        schema_extra = {
            "example": {
                "studentID" : 1,
                "academmicClassId": 1,
                "createDate": "12/12/1999"
            }
        }