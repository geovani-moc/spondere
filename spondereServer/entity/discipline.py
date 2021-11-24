from fastapi.param_functions import Body
from pydantic.main import BaseModel

class Discipline(BaseModel):
    code:str = None
    semesterCode: str = None
    name:str = None
    description:str = None

    class Config:
        schema_extra = {
            "example": {
                "code": "dfbn2",
                "semesterCode": "2332nk",
                "name": "Introdução a tecnicas de Planilha.",
                "description": "Historia e estudo do uso da planilha."
            }
        }
