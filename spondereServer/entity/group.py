from pydantic.main import BaseModel
from pydantic.main import BaseModel

class Group(BaseModel):
    classCode:str = None
    professorCode: str = None
    studentCode: str = None

    class Config:
        schema_extra = {
            "example":{
                "classCode": "122a",
                "professorCode": "aan12",
                "studentCode": "ond21"
            }
        }