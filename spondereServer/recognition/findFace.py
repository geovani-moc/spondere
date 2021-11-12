import os
import cv2 as cv
from settings import FACE_DIM, MIN_SIZE_DATASET, faceCascade, eyeCascade
from util.image import loadUserDataset


def findFace(image):
    facesPositions = faceCascade.detectMultiScale(image)
    #eyesPositions = eyeCascade.detectMultiScale(image)
    
    if len(facesPositions) > 0:
        column, row, width, height = facesPositions[0]
    else:
        return None, 'Erro ao localizar face, não existe faces na imagem. \n'

    #face(column, row, width, height)
    #localiza a maior regiao area que é cnsiderada uma face
    for face in facesPositions:
        if height < face[3]:
            column, row, width, height = face

    #vericar todos os olhos que estão dentro da maior área considerada uma face

    #caso exista dois olhos alinhar, c.c. retornar erro.

    #antes de recortar realizar o alinhamento da face

    # olhar se é necessario força que os olhos fiquem em uma posição especifica
    # para que haja um padrão no eigenface (sem sobreposições)
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
        return None, "Quantidade de olhos localizados é insuficiente"
    
    return eyesChecked, None


#salvar imagem interira enviada do dataset, extrair face no momento do treinamento

def storeDataset(data, destiny, label):
    path = destiny + "/" + label
    for image in data:
        if image is None:
            return "erro em salvar imagens da face"

        if not os.path.isdir(path, image):
            try:
                os.mkdir(path)
            except OSError:
                print ("Erro na criação do diretotio: %s" % path)
            else:
                pass
        
        cv.imwrite(path, image)

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