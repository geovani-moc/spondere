
from pydantic.main import BaseModel


class Discipline(BaseModel):
    code:str
    perioCode: str
    name:str
    description:str
