import numpy as np
import os
from recognition.findFace import extractFace
from settings import MIN_SIZE_DATASET
from skimage.feature import local_binary_pattern

def train(path, userID):
    if os.path.exists(path+"/"+userID+'/lbp.txt'):
        features = np.loadtxt(path+"/"+userID+'/lbp.txt', float)   
        return features, None 
    
    return updateTrain(path, userID)

def updateTrain(path, userID):
    images, error = extractFace(path, userID)

    if error is not None:return None, error
    if len(images) < MIN_SIZE_DATASET:
        return None, "O usuario não tem imagens sufucientes com a face detectavel."

    features = []
    for image in images:
        feature = extractFeature(image)
        features.append(feature)
    
    dataFeatures = np.array(features, float)
    np.savetxt(path+"/"+userID+'/lbp.txt', dataFeatures)

    return  dataFeatures, None

def extractFeature(image):
    lbp = local_binary_pattern(image, 8,1.0,method='default')

    return None