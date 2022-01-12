from datetime import datetime
from typing import Optional
from pydantic.main import BaseModel

class Group(BaseModel):
    id:int = None
    code:int = None
    beginDate:Optional[datetime] = None
    endDate:Optional[datetime] = None
    deactivate:bool = None
    disciplineID:Optional[int] = None

    class Config:
        schema_extra = {
            "example":{
                "beginDate": "12/12/1999",
                "endDate": "01/06/2000",
                "deactivate": "false"
            }
        }