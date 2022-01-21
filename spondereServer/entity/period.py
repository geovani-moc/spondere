from typing import Optional
from pydantic.main import BaseModel
from datetime import datetime

class Period(BaseModel):
    id:int = None
    code:str = None
    active:bool = None
    beginDate: Optional[datetime] = None
    endDate: Optional[datetime] = None

    class Config:
        schema_extra = {
            "example":{
                "code": "2022/1",
                "active": True,
                "beginDate": "2022, 01, 31, 15, 46, 59, 24384",
                "endDate": "2022, 06, 31, 15, 46, 59, 24384"
            }
        }
