from settings import(
    PATH_DATA_TRAIN,
    PATH_IMAGES,
    MIN_SIZE_DATASET
)
import os
import numpy as np
from recognition.findFace import extractFace

def loadFullTrain(trainName, method):
    path = PATH_DATA_TRAIN
    if os.path.exists(path + trainName + ".txt"):
        features = np.loadtxt(path + trainName + ".txt", float)
        return features, None
    features = []
    errors = []  
    
    directories = os.listdir(PATH_IMAGES)
    for directorie in directories:
        if os.path.isdir(os.path.join(PATH_IMAGES, directorie)):
            feature, error = train(PATH_IMAGES, directorie, method)
            if error is not None:
                errors.append(error)
            features.append(feature)
                
    return features, errors

def loadFullLabels():
    path = PATH_DATA_TRAIN
    if os.path.exists(path + '/labels.txt'):
        labels = np.loadtxt(path+"/labels.txt", str)
        return labels
    
    labels = []
    directories = os.listdir(PATH_IMAGES)
    for directorie in directories:
        if os.path.isdir(os.path.join(PATH_IMAGES, directorie)):
            labels.append(directorie)
    
    return labels

def updateTrain(path, userID, methodExtractFeature):
    images, error = extractFace(path, userID)

    if error is not None:return None, error
    if len(images) < MIN_SIZE_DATASET:
        return None, "O usuario não tem imagens sufucientes com a face detectavel."

    features = []
    for image in images:
        feature = methodExtractFeature(image)
        features.append(feature)
    
    dataFeatures = np.array(features, float)
    np.savetxt(path+"/"+userID+'/lbp.txt', dataFeatures)

    return  dataFeatures, None

def train(path, userID, method):

    if os.path.exists(path+"/"+userID+'/eigen.txt'):
        features = np.loadtxt(path+"/"+userID+'/eigen.txt', float)   
        return features, None 

    return updateTrain(path, userID, method)