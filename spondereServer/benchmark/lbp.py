from util.image import printFeature
import numpy as np
import os
import cv2 as cv
from recognition.findFace import extractFace

def train(path, userID, printDebug = False):
    if os.path.exists(path+"/"+userID+'/data.txt'):
        features = np.loadtxt(path+"/"+userID+'/data.txt', float)   
        return features, None 
    
    images, error = extractFace(path, userID)

    if error is not None:
        return None, error
    
    if images[0] is None:
        return None, "Erro no treinamento, imagens nulas."

    #data = covarianceMatrix(images)
    #features, _ = cv.PCACompute(data, mean=None, maxComponents=numberComponents) 

    if features.ndim == 2:
        features = features[0] 
    
    if printDebug:
        printFeature(features, images[0].shape, 'Treino: '+userID)
    
    dataFeatures = np.array(features, float)
    np.savetxt(path+"/"+userID+'/data.txt', dataFeatures, fmt='%1.5f')

    return features, None

def updateTrain(path, userID):
    images, error = extractFace(path, userID)

    if error is not None:
        return error
    
    if images[0] is None:
        return None, "Erro no treinamento, imagens nulas."

    #data = covarianceMatrix(images)
    #features, _ = cv.PCACompute(data, mean=None, maxComponents=numberComponents) 
    
    dataFeatures = np.array(features, int)
    np.savetxt(path+"/"+userID+'/data.txt', dataFeatures)

    return  None
