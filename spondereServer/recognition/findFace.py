import cv2 as cv
from settings import FACE_DIM, MIN_SIZE_DATASET, faceCascade
from util.image import loadUserDataset
import numpy as np


def findFace(image):
    imageGrayScale = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    facesPositions = faceCascade.detectMultiScale(imageGrayScale)
    
    if len(facesPositions) > 0:
        column, row, width, height = facesPositions[0]
    else:
        return None, 'Erro ao localizar face, não existe faces na imagem. \n'

    #face(column, row, width, height)
    #a regiao com maior area é considerada uma face de interesse
    for face in facesPositions:
        if height < face[3]:
            column, row, width, height = face

    cropFace = image[ row: row+height, column:column+width]
    cropFace = cv.resize(cropFace, (FACE_DIM, FACE_DIM))    

    return np.asarray(cropFace), None

def extractFace(path:str, userID:int):
    images = loadUserDataset(path, userID)
    faces = []

    for image in images:
        face, error = findFace(image)
        if error is None:
            faces.append(face)
    
    if len(faces) < MIN_SIZE_DATASET:
        return None, "quantidade pequena de imagens no dataset"

    return faces, None