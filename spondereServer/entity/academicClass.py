from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel

class AcademicClass(BaseModel):
    id:int = None
    groupID:int = None
    titleClass:Optional[str] = None
    descriptionClass:Optional[str] = None
    beginDate: Optional[datetime] = None
    endDate: Optional[datetime] = None
    validationStatus:Optional[int] = None
    validationType:Optional[int] = None
    validationCode:Optional[str] = None

    class Config:
        schema_extra = {
            "example":{
                "groupID": 1,
                "titleCLass": "p = np",
                "beginDate": "2021, 11, 24, 15, 46, 3, 301046",
                "endDate": "2021, 11, 24, 15, 46, 59, 24384",
                "professorCode": "kskdk2"
            }
        }