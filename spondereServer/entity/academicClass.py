from datetime import datetime

class AcademicClass:
    code:int = None
    disciplineCode: str = None
    beginDate: datetime = None
    endDate: datetime = None
    professorCode: str = None

    class Config:
        schema_extra = {
            "example":{
                "code": 0,
                "disciplineCode": "0932fsds",
                "beginDate": "02/01/2001",
                "endDate": "01/01/2021",
                "professorCode": "kskdk2"
            }
        }