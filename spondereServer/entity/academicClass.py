from typing import Optional
from pydantic.main import BaseModel

class AcademicClass(BaseModel):
    id:int = None
    groupID:int = None
    titleClass:str = None
    descriptionClass:str = None
    beginDate: Optional[str] = None
    endDate: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    activeValidation:bool= None
    validationByQrCode:bool = None
    validationByBLE:bool = None
    blockedAttendance:bool = None
    validationCode:Optional[str] = None

    class Config:
        schema_extra = {
            "example":{
                "groupID": 1,
                "titleClass": "Integral",
                "descriptionClass": "Aula 2.",
                "beginDate": "2022-10-19 10:10:00+2",
                "endDate": "2022-10-19 12:00:00+2",
                "activeValidation": False,
                "validationByQrCode": False,
                "validationByBLE": False,
                "blockedAttendance": False
            }
        }