import os, shutil
from fastapi import HTTPException
from settings import PATH_IMAGES

def createUserImagesPath(studentID:int)->str:
    path:str = PATH_IMAGES + '/' + str(studentID)
    return path

def removeAllFilesInFolder(folder:str):
    for filename in os.listdir(folder):
        filePath = os.path.join(folder, filename)
        try:
            if os.path.isfile(filePath) or os.path.islink(filePath):
                os.unlink(filePath)
            elif os.path.isdir(filePath):
                shutil.rmtree(filePath)
        except Exception as e:
            print('%s -> %s' % (filePath, e))
            raise HTTPException(status_code=401,
                detail="Falha ao deletar imagem da biometria.")
            