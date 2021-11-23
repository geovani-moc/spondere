import cv2 as cv
from settings import FACE_DIM, MIN_SIZE_DATASET, faceCascade
from util.image import loadUserDataset


def findFace(image):
    facesPositions = faceCascade.detectMultiScale(image)
    
    if len(facesPositions) > 0:
        column, row, width, height = facesPositions[0]
    else:
        return None, 'Erro ao localizar face, não existe faces na imagem. \n'

    #face(column, row, width, height)
    #localiza a maior regiao area que é cnsiderada uma face
    for face in facesPositions:
        if height < face[3]:
            column, row, width, height = face

    cropFace = image[ row: row+height, column:column+width]
    cropFace = cv.resize(cropFace, (FACE_DIM, FACE_DIM))    

    return cropFace, None

def extractFace(path, userID):
    images = loadUserDataset(path, userID)
    faces = []

    for image in images:
        face, error = findFace(image)
        if error is None:
            faces.append(face)
    
    if len(faces) < MIN_SIZE_DATASET:
        return None, "quantidade pequena de imagens no dataset"

    return faces, None