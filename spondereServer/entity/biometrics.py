
from typing import List
from datetime import datetime
from pydantic.main import BaseModel

#pesquisar sobre o Optional da biblioteca typing
class Biometrics(BaseModel):
    code: str = None
    feature: List[int] = None
    createDate: datetime = None
    status: bool = None
    studentCode: str = None
