from datetime import datetime
from typing import Any, List

from fastapi.param_functions import Body

class Frequency:
    studentCode: str = None
    academicClassCode: str = None
    method:int = None
    createDate: datetime = None
    geolocalization: str = None
    validationType: int = None
    photo:List[int] = None

    #checar os detalhes sobre datas e horas

    class Config:
        schema_extra = {
            "example": {
                "studentCode" : "fdkn3",
                "academmicClassCode": "434mnd",
                "method": 1,
                "createDate": "12/12/1999",
                "geolocalization": "72.32323, 23.43438",
                "validationType": 2
            }
        }