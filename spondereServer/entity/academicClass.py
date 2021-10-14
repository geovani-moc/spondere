from datetime import datetime

class AcademicClass:
    disciplineCode: str = None
    beginDate: datetime = None
    endDate: datetime = None
    codeProfessor: str = None

    class Config:
        schema_extra = {
            "example":{
                "disciplineCode": "0932fsds",
                "beginDate": "02/01/2001",
                "endDate": "01/01/2021",
                "codeProfessor": "kskdk2"
            }
        }