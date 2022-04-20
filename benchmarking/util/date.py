from datetime import datetime

def isSmaller(beginDate:str, endDate:str)->bool:
    date1 = datetime.fromisoformat(beginDate)
    date2 = datetime.fromisoformat(endDate)
    return date1 < date2

