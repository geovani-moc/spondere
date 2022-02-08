from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel

class AcademicClass(BaseModel):
    id:int = None
    groupID:int = None
    titleClass:Optional[str] = None
    descriptionClass:Optional[str] = None
    beginDate: Optional[str] = None
    endDate: Optional[str] = None
    activeValidation:Optional[bool] = None
    validationByQrCode:Optional[bool] = None
    validationByBLE:Optional[bool] = None
    validationCode:Optional[str] = None

    class Config:
        schema_extra = {
            "example":{
                "groupID": 1,
                "titleClass": "Integral",
                "descriptionClass": "Aula 2.",
                "beginDate": "25-02-2022 12:01",
                "endDate": "25-02-2022 14:01",
                "activeValidation": False,
                "validationByQrCode": False,
                "validationByBLE": False,
                "validationCode": "AAAPPPUUU1"
            }
        }