from util.image import printFeature
import numpy as np
from settings import EIGENFACES_NUMBER_COMPONENTS
import os
import cv2 as cv
from recognition.findFace import extractFace

def train(path, userID, numberComponents = EIGENFACES_NUMBER_COMPONENTS, printDebug = False):
    if os.path.exists(path+"/"+userID+'/data.npy'):
        features = np.load(path+"/"+userID+'/data.npy')   
        return features, None 
    
    images, error = extractFace(path, userID)

    if error is not None:
        return None, error
    
    if images[0] is None:
        return None, "Erro no treinamento, imagens nulas."

    data = covarianceMatrix(images)
    features, _ = cv.PCACompute(data, mean=None, maxComponents=numberComponents) 

    if features.ndim == 2:
        features = features[0] 
    
    if printDebug:
        printFeature(features, images[0].shape, 'Treino: '+userID)
    
    dataFeatures = np.array(features, dtype=float)
    np.save(path+"/"+userID+'/data.npy', dataFeatures, fmt='%1.5f')

    return features, None

def updateTrainUser(path, userID, numberComponents = EIGENFACES_NUMBER_COMPONENTS):
    images, error = extractFace(path, userID)

    if error is not None:
        return error
    
    if images[0] is None:
        return "Erro no treinamento, imagens nulas."

    data = covarianceMatrix(images)
    features, _ = cv.PCACompute(data, mean=None, maxComponents=numberComponents) 
    
    dataFeatures = np.array(features, dtype=int)
    np.save(path+"/"+userID+'/data.npy', dataFeatures)

    return  None

def covarianceMatrix(images):
    numberImages = len(images)
    shape = images[0].shape

    data = np.zeros((numberImages, shape[0]* shape[1]), dtype = np.float32)

    for number in range(0, numberImages):
        image = images[number].flatten()
        data[number,:] = image

    return data

