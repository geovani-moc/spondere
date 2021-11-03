from util.image import printFeature
import numpy as np
from settings import (
    EIGENFACES_NUMBER_COMPONENTS,
    MIN_SIZE_DATASET)
import os
import cv2 as cv
from recognition.findFace import extractFace

def train(path, userID):

    if os.path.exists(path+"/"+userID+'/eigen.txt'):
        features = np.loadtxt(path+"/"+userID+'/eigen.txt', float)   
        return features, None 
    
    return updateTrain(path, userID)

def updateTrain(path, userID):
    images, error = extractFace(path, userID)

    if error is not None:
        return None, error
    
    if len(images) < MIN_SIZE_DATASET:
        return None, "O usuario não tem imagens sufucientes com a face detectavel."

    data = covarianceMatrix(images)
    features, _ = cv.PCACompute(data, mean=None, maxComponents=EIGENFACES_NUMBER_COMPONENTS) 

    if features.ndim == 2:
        features = features[0] 
        
    dataFeatures = np.array(features, float)
    np.savetxt(path+"/"+userID+'/eigen.txt', dataFeatures, fmt='%1.5f')

    return features, None


def covarianceMatrix(images):
    numberImages = len(images)
    shape = images[0].shape

    data = np.zeros((numberImages, shape[0]* shape[1]), dtype = np.float32)

    for number in range(0, numberImages):
        image = images[number].flatten()
        data[number,:] = image

    return data

