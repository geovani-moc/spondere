from pydantic.main import BaseModel

class Period(BaseModel):
    id:int = None
    code:str = None
    active:bool = None
    beginDate: str = None
    endDate: str = None

    class Config:
        schema_extra = {
            "example":{
                "code": "2022/1",
                "active": True,
                "beginDate": "2022-02-13 10:10:00+2",
                "endDate": "2022-07-25 10:10:00+2"
            }
        }
