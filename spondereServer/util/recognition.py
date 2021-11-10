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
        features = np.load(path + trainName + ".txt")
        return features, None
    features = []
    errors = []  
    
    directories = os.listdir(PATH_IMAGES)
    for directorie in directories:
        if os.path.isdir(os.path.join(PATH_IMAGES, directorie)):
            feature, error = train(PATH_IMAGES, directorie, method, trainName)
            if error is not None:
                errors += error
            features.append(feature)
                
    return features, errors

def loadFullLabels():
    path = PATH_DATA_TRAIN
    if os.path.exists(path + '/labels.txt'):
        labels = np.load(path+"/labels.txt")
        return labels
    
    labels = []
    directories = os.listdir(PATH_IMAGES)
    for directorie in directories:
        if os.path.isdir(os.path.join(PATH_IMAGES, directorie)):
            labels.append(directorie)
    
    return labels

def updateTrain(path, userID, methodExtractFeature, name):
    images, error = extractFace(path, userID)

    if error is not None: return None, [error]
    if len(images) < MIN_SIZE_DATASET:
        return None, ["O usuario não tem imagens sufucientes com a face detectavel."]

    errors = []
    features = []
    for image in images:
        feature, error = methodExtractFeature(image)
        if error is not None: errors.append(error)
        features.append(np.array(feature, float))
    
    dataFeatures = np.array(features, dtype=object)

    np.save(path + '/' + userID + '/' + name + '.txt', dataFeatures)

    return  dataFeatures, errors

def train(path, userID, method, name="eigen"):

    if os.path.exists(path+"/"+userID+'/' + name + '.txt'):
        features = np.load(path+"/"+userID+'/' + name + '.txt')   
        return features, None 

    return updateTrain(path, userID, method, name)

def deleteTrain(name):
    dirs = os.listdir(PATH_IMAGES)
    for dir in dirs:
        if os.path.isdir(os.path.join(PATH_IMAGES, dir)):
            if os.path.exists(os.path.join(PATH_IMAGES, dir, name+'.txt')):
                os.remove(os.path.join(PATH_IMAGES, dir, name+'.txt'))

