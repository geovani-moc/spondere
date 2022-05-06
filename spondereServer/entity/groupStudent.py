from pydantic.main import BaseModel

class GroupStudent(BaseModel):
    studentUsername:str = None
    groupID:int = None
    
    class Config:
        schema_extra = {
            "example":{
                "studentUsername": "estudante01",
                "groupID": 1,
            }
        }
