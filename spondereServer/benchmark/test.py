from recognition.findFace import extractFace
from benchmark.eigenfaces import covarianceMatrix
from settings import (
    EIGENFACES_NUMBER_COMPONENTS, 
    PATH_IMAGES, 
    PATH_DATA_TRAIN, 
    EIGENFACES, 
    HOG, 
    LBP, 
    EUCLEDIAN_DISTANCE, 
    KNN, 
    SVM)
import numpy as np
import cv2 as cv
import os

def recognitionFace(
    path=PATH_IMAGES, 
    pathDataTrain=PATH_DATA_TRAIN, 
    featureType=EIGENFACES, 
    extractType=EUCLEDIAN_DISTANCE):

    features = []
    labels = []

    if (os.path.exists(path+"/feature.txt") and
        os.path.exists(path+"/labels.txt")):
        features = np.loadtxt(pathDataTrain+"/feature.txt", float)
        labels = np.loadtxt(pathDataTrain+"/labels.txt", str)
    
    error = train(path, pathDataTrain, featureType)
    if error is not None:
        return None, error

    features = np.loadtxt(pathDataTrain+"/feature.txt", float)
    labels = np.loadtxt(pathDataTrain+"/labels.txt", str)

    #fazer a parte de algoritmos KNN, SMV e distancia euclidiana

    
    return True, None


    
    
def train(path = PATH_IMAGES, pathDataTrain = PATH_DATA_TRAIN, featureType = EIGENFACES):
    fullPath = './'+path+'/'
    directories = os.listdir(fullPath)

    errors = []
    dataFeatures = []
    labels = []

    for directory in directories:
        if os.path.isdir(fullPath + directory):

            feature, error = loadTrainUser(directory, path, featureType)

            if error is None:
                labels.append(directory)
                dataFeatures.append(feature)
            else:
                errors.append(error)
    
    dataFeatures = np.array(dataFeatures, float)

    np.savetxt(pathDataTrain+"/feature.txt", dataFeatures, fmt='%1.5f')
    np.savetxt(pathDataTrain+"/labels.txt", labels, delimiter=" ", fmt='%s')
    
    if len(errors) == 0:
        return None

    return errors

def loadTrainUser(userID, path=PATH_IMAGES, featureType = EIGENFACES):
    if os.path.exists(path+"/"+userID):
        if os.path.exists(path+"/"+userID+'/data.txt'):
            features = np.loadtxt(path+"/"+userID+'/data.txt', float)
            return features, userID, None    
            
        features, userID, error = updateUserDataTrain(userID, path=path, featureType = featureType)
        if error is not None:
            return None, None, error

        return features, userID, None 
    
    return None, None, 'O usuario '+userID+ 'não existe.'



def updateUserDataTrain(userID, path = PATH_IMAGES, featureType=EIGENFACES):
    images, error = extractFace(path, userID)

    if error is not None:
        return None, None, error 
    if images[0] is None:
        return None, None, "Erro no treinamento, imagens nulas."
    
    features = []
    
    #falta implementar hog e lbp
    if featureType == EIGENFACES:
        data = covarianceMatrix(images)
        features, _ = cv.PCACompute(data, mean=None, maxComponents=EIGENFACES_NUMBER_COMPONENTS) 
    elif featureType == HOG:
        pass
    elif featureType == LBP:
        pass
    else:
        return None, None, 'Erro na atualização do treinamento, tipo de caracterista não existe: ' + featureType
        
    dataFeatures = np.array(features, int)
    np.savetxt(path+"/"+userID+'/data.txt', dataFeatures)

    return  dataFeatures, userID, None

def updateAllUserDataTrain(path= PATH_IMAGES):
    fullPath = './'+path+'/'
    directories = os.listdir(fullPath)

    errors = []

    for directory in directories:
        if os.path.isdir(fullPath + directory):

            _, _, error = updateUserDataTrain(directory)

            if error is not  None:
                errors.append(error)
    
    if len(errors) > 1:
        return errors
    
    return None



if __name__ == '__main__':
    pass
