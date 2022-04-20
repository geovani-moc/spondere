import os
import cv2 as cv
from settings import FACE_DIM, PATH_IMAGES, faceCascade, eyeCascade
import numpy as np
from recognition.findFace import findFace as fc

def findFace(image):
    facesPositions = faceCascade.detectMultiScale(image)
    eyesPositions = eyeCascade.detectMultiScale(image)
    
    if len(facesPositions) > 0:
        column, row, width, height = facesPositions[0]
    else:
        return None, 'Erro ao localizar face, não existe faces na imagem. \n'

    #face(column, row, width, height)
    #localiza a maior regiao area que é cnsiderada uma face
    for face in facesPositions:
        if height < face[3]:
            column, row, width, height = face

    eyeLeft, eyeRight, error = checkEyes(eyesPositions, column, row, width, height)
    if error is not None: return None, error 

    eyeLeftCenter = (int(eyeLeft[0]+ (eyeLeft[2]/2)), int(eyeLeft[1]+(eyeLeft[3]/2)))
    eyeRightCenter = (int(eyeRight[0]+ (eyeRight[2]/2)), int(eyeRight[1]+(eyeRight[3]/2)))

    
    delta_x = eyeRightCenter[0] - eyeLeftCenter[0]
    delta_y = eyeRightCenter[1] - eyeLeftCenter[1]
    angle = np.arctan(delta_y / delta_x)
    angle = (angle * 180) / np.pi

    h, w = image.shape[:2]
    center = (w // 2, h // 2)
    matrixRotation = cv.getRotationMatrix2D(center, (angle), 1.0)

    image = cv.warpAffine(image, matrixRotation, (w, h))
    #recortar apartir do centro dos olhos para mehor resultado

    cropFace = image[ row: row+height, column:column+width]
    cropFace = cv.resize(cropFace, (FACE_DIM, FACE_DIM))    

    return cropFace, None

#testar a funcão
def checkEyes(eyes, column, row, width, height):
    eyesChecked = []
    for (eyeColumn, eyeRow, eyeWidth, eyeHeight) in eyes:
        if (eyeColumn >= column and 
                eyeColumn <= column+width and
                eyeRow >= row and
                eyeRow <= row+height):
            eyesChecked.append([eyeColumn, eyeRow, eyeWidth, eyeHeight])

    if len(eyesChecked) != 2:
        return None, None, "Quantidade de olhos localizados é insuficiente"

    eyeLeft = eyesChecked[0]
    eyeRight = eyesChecked[1]

    if eyeLeft[0] > eyeRight[0]:
        eyeLeft, eyeRight = eyeRight, eyeLeft

    return eyeLeft, eyeRight, None


if __name__ == '__main__':
    #image = cv.imread('./static/image/eu.jpg')
    image = cv.imread(os.path.join(PATH_IMAGES, 's01/11.jpg'))
    aux, _ = fc(image)
    (h, w) = image.shape[:2]
    height = 480
    r = height / float(h)
    dim = (int(w * r), height)
    image = cv.resize(image, dim)

    image, error = findFace(image)
    if error is not None: 
        print(error)
    else:
        #image = cv.resize(image, (300,300))
        cv.imshow("alinhada", image)
        cv.imshow("sem alinhar", aux)
        cv.waitKey() 