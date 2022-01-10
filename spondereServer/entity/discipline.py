from pydantic.main import BaseModel

class Discipline(BaseModel):
    id:int = None
    semesterID: int = None
    name:str = None
    description:str = None

    class Config:
        schema_extra = {
            "example": {
                "semesterCode": 1,
                "name": "Introdução a tecnicas de Planilha.",
                "description": "Historia e estudo do uso da planilha."
            }
        }
