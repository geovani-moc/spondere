from datetime import datetime
from typing import Optional
from xmlrpc.client import boolean

from pydantic.main import BaseModel

class AcademicClass(BaseModel):
    id:int = None
    groupID:int = None
    titleClass:Optional[str] = None
    descriptionClass:Optional[str] = None
    beginDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    activeValidation:Optional[bool] = None
    validationByQrCode:Optional[bool] = None
    validationByBLE:Optional[bool] = None
    validationCode:Optional[str] = None

    class Config:
        schema_extra = {
            "example":{
                "groupID": 1,
                "titleCLass": "p = np",
                "descriptionClass": "Introdução a complexidade de classes de problemas.",
                "beginDate": "2021, 11, 24, 15, 46, 3, 301046",
                "endDate": "2021, 11, 24, 15, 46, 59, 24384",
                "activeValidation": False,
                "validationByQrCode": False,
                "validationByBLE": False,
                "validationCode": "kskdk2"
            }
        }