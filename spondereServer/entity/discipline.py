
from pydantic.main import BaseModel


class Discipline(BaseModel):
    code:str
    semesterCode: str
    name:str
    description:str

    class Config:
        schema_extra = {
            "example": {
                "code": "dfbn2",
                "semesterCode": "2332nk",
                "name": "Introdução a tecnicas de Planilha.",
                "description": "Historia e estudo do uso da planilha."
            }
        }
