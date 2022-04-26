import os
import glob
import cv2 as cv
import numpy as np
from settings import(
    faceCascade,
    FACE_DIM,
    PATH_IMAGES
)
from benchmark.cnn import (
    verifyFace,
    euclidianDistance,
    knn_1, svm_linear, svm_no_linear
)

def test(classifier, path=PATH_IMAGES)->float:
    count:float = 0
    hits:float = 0 
    directories = os.listdir(path)

    for directorie in directories:
        if os.path.isdir(os.path.join(path, directorie)):
            if (os.path.exists(os.path.join(path, directorie, 'false')) and 
                os.path.exists(os.path.join(path, directorie, 'true'))):
                
                tempCount, tempHits = testImages(os.path.join(path, directorie, 'false'), directorie, classifier)
                count = count + tempCount
                hits = hits + (tempCount - tempHits)

                tempCount, tempHits = testImages(os.path.join(path, directorie, 'true'), directorie, classifier)
                count += tempCount
                hits += tempHits

    if count == 0: return 0.0

    print(f'acertos:{hits}\nQuantidade:{count}')

    return (hits/count)

def testImages(path, userID, classifier):
    directories = os.listdir(path)
    hits:float = 0

    for directory in directories:
        image, error = loadFace(os.path.join(path, directory))
        if error == None:
            result,_ = verifyFace(image, userID, classifier)
            if result: hits+=1
        else:
            print("A face testada não foi reconhecida")
        
    count:float =  float(len(glob.glob1(path,"*.jp*")))
    return count, hits

def loadFace(path):
    image = cv.imread(path)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    return findFace(image)

def findFace(image):
    imageGrayScale = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    facesPositions = faceCascade.detectMultiScale(imageGrayScale)
    
    if len(facesPositions) > 0:
        column, row, width, height = facesPositions[0]
    else:
        return None, 'Erro ao localizar face, não existe faces na imagem. \n'

    for face in facesPositions:
        if height < face[3]:
            column, row, width, height = face

    cropFace = image[row: row+height, column:column+width]
    cropFace = cv.resize(cropFace, (FACE_DIM, FACE_DIM))    

    return np.asarray(cropFace), None

def CNNTests():
    acurracy = test(euclidianDistance)
    print(f'Distancia euclidiana: {acurracy*100}%')

    acurracy = test(knn_1)
    print(f'KNN(k=1): {acurracy*100}%')

    acurracy = test(svm_linear)
    print(f'SVM(linear): {acurracy*100}%')

    acurracy = test(svm_no_linear)
    print(f'SVM(não linear): {acurracy*100}%')