from typing import Optional
from pydantic.main import BaseModel
from datetime import datetime

class Period(BaseModel):
    id:int = None
    code:str = None
    deactivate:bool = None
    beginDate: Optional[datetime] = None
    endDate: Optional[datetime] = None