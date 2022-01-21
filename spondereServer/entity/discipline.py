from pydantic.main import BaseModel

class Discipline(BaseModel):
    id:int = None
    code:str = None
    name:str = None
    description:str = None

    class Config:
        schema_extra = {
            "example": {
                "code": "BCC20A",
                "name": "Introdução a tecnicas de Planilha.",
                "description": "Historia e estudo do uso da planilha."
            }
        }
