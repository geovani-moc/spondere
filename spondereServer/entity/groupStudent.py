from pydantic.main import BaseModel

class GroupStudent(BaseModel):
    studentUsername:str = None
    groupID:int = None
    
    class Config:
        schema_extra = {
            "example":{
                "studentUsername": "mari",
                "group": "1",
            }
        }
