import random
from settings import VALIDATION_CODE_SIZE

def generateValidationCode()->str:
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    number = "1234567890"

    allChars = lower + number + upper
    code = "".join(random.sample(allChars, VALIDATION_CODE_SIZE))
    return code


