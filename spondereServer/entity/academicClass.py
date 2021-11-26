from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel

class AcademicClass(BaseModel):
    code:int = None
    disciplineCode: str = None
    beginDate: datetime = None
    endDate: Optional[datetime] = None
    professorCode: str = None

    class Config:
        schema_extra = {
            "example":{
                "code": 0,
                "disciplineCode": "0932fsds",
                "beginDate": "2021, 11, 24, 15, 46, 3, 301046",
                "endDate": "2021, 11, 24, 15, 46, 59, 24384",
                "professorCode": "kskdk2"
            }
        }