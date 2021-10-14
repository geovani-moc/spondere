from pydantic.utils import ClassAttribute


class Group:
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