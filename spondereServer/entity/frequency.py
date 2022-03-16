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
    createDate:str = None
    validationCode:str = None
    latitude:Optional[float] = None
    longitude:Optional[float] = None
    failure:Optional[str] = None
    photo:List[bytes] = None

    class Config:
        schema_extra = {
            "example": {
                "studentID" : 1,
                "academmicClassId": 1,
                "ManualAttendance": True,
                "BLEAttendance": False,
                "QrCodeAttendance": False,
                "createDate": "2021-10-19 10:23:54+2"
            }
        }

class FrequencyList(BaseModel):
    groupID:int = None
    studentID:int = None
    fullName:str = None
    frequencyID:int = None
    isManual:bool = None
