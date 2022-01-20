from pydantic.main import BaseModel

class GroupProfessor(BaseModel):
    professorUsername:str = None
    groupID:int = None
    
    class Config:
        schema_extra = {
            "example":{
                "professorUsername": "mari",
                "group": "1",
            }
        }
