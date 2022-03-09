import os, shutil
from fastapi import HTTPException
from settings import PATH_IMAGES

def createUserImagesPath(studentID:int)->str:
    path:str = PATH_IMAGES + '/' + str(studentID)
    return path

def removeAllFilesInFolder(folder:str):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('%s -> %s' % (file_path, e))
            raise HTTPException(status_code=401,
                detail="Falha ao deletar imagem da biometria.")
            