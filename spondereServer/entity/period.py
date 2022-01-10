from typing import Optional
from pydantic.main import BaseModel
from datetime import datetime

class Period(BaseModel):
    id:int = None
    beginDate: Optional[datetime] = None
    endDate: Optional[datetime] = None