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
                "name": "Nome de uma disciplina.",
                "description": "Descrição de uma disciplina."
            }
        }
