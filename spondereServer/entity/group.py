from pydantic.main import BaseModel

class Group(BaseModel):
    id:int = None
    code:str = None
    active:bool = None
    semesterID:int = None
    disciplineID:int = None

    class Config:
        schema_extra = {
            "example":{
                "code":"codDiscplina001",
                "semesterID":1,
                "active": "true",
                "disciplineID":1
            }
        }