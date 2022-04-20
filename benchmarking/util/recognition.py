from settings import(
    PATH_DATA_TRAIN,
    PATH_IMAGES,
    MIN_SIZE_DATASET, 
    NUMBER_FEATURES_DATASET
)
import os
import numpy as np
from recognition.findFace import extractFace

def loadFullTrain(trainName, method, args):
    path = PATH_DATA_TRAIN
    if os.path.exists(os.path.join(path, trainName+'.npy')):
        features = np.load(os.path.join(path, trainName + '.npy'))
        return features, None
    features = []
    errors = []  
    
    directories = os.listdir(PATH_IMAGES)
    for directorie in directories:
        if os.path.isdir(os.path.join(PATH_IMAGES, directorie)):
            featuresUser, error = train(PATH_IMAGES, directorie, method, trainName, args)
            if error is not None:
                errors += error
            if featuresUser is not None:
                features.append(featuresUser)

    if(not os.path.exists(path)):
        os.mkdir(path)
    
    features = np.array(features, dtype=float)
    np.save(os.path.join(path, trainName+'.npy'), features)
                
    return features, errors

def readAllTrains(trainName, method):
    path = PATH_DATA_TRAIN
    features = []
    errors = []  
    
    directories = os.listdir(PATH_IMAGES)
    for directorie in directories:
        if os.path.isdir(os.path.join(PATH_IMAGES, directorie)):
            featuresUser, error = train(PATH_IMAGES, directorie, method, trainName)
            if error is not None:
                errors += error
            if featuresUser is not None:
                features.append(featuresUser)

    if(not os.path.exists(path)):
        os.mkdir(path)
    
    features = np.array(features, dtype=float)
    np.save(os.path.join(path, trainName+'.npy'), features)
                
    return features, errors

def loadFullLabels(name):
    path = PATH_DATA_TRAIN
    if os.path.exists(os.path.join(path, 'labels.npy')):
        labels = np.load(os.path.join(path, 'labels.npy'))
        return labels
    
    labels = []
    directories = os.listdir(PATH_IMAGES)
    for directorie in directories:
        if os.path.isdir(os.path.join(PATH_IMAGES, directorie)):
            if os.path.exists(os.path.join(PATH_IMAGES, directorie, name+'.npy')):
                labels.append(directorie)
    
    np.save(os.path.join(path, 'labels.npy'), labels)
    
    return labels

def readAllLabels(name:str):
    path = PATH_DATA_TRAIN   
    labels = []
    directories = os.listdir(PATH_IMAGES)
    for directorie in directories:
        if os.path.isdir(os.path.join(PATH_IMAGES, directorie)):
            if os.path.exists(os.path.join(PATH_IMAGES, directorie, name+'.npy')):
                labels.append(directorie)
    
    np.save(os.path.join(path, 'labels.npy'), labels)
    
    return labels

def updateTrain(path:str, userID:int, methodExtractFeature, name:str, args):
    faces, error = extractFace(path, userID)

    if error is not None: return None, error
    if len(faces) < MIN_SIZE_DATASET:
        return None, "r003"

    features = methodExtractFeature(faces, args)
    
    if name == 'eigen':
        if len(features) != 1:
            return None, "r004"
    else:
        if len(features) < MIN_SIZE_DATASET:
            return None, "r004"
        features = normalizeFeatures(features)

    features = np.array(features, dtype=float)
    np.save(path + '/' + str(userID) + '/' + name + '.npy', features)

    return  features, error

def normalizeFeatures(features):
    if len(features) > NUMBER_FEATURES_DATASET:
        return features[0:NUMBER_FEATURES_DATASET]

    if len(features) < NUMBER_FEATURES_DATASET:
        for i in range(len(features), NUMBER_FEATURES_DATASET):
            features = np.concatenate((features, [features[0]]))

    return features

def train(path:str, userID:int, method, name, args):
    if os.path.exists(path+"/"+str(userID)+'/' + name + '.npy'):
        features = np.load(path+"/"+str(userID)+'/' + name + '.npy')   
        return features, None 

    return updateTrain(path, userID, method, name, args)

def deleteTrain(name:str):
    dirs = os.listdir(PATH_IMAGES)
    for dir in dirs:
        if os.path.isdir(os.path.join(PATH_IMAGES, dir)):
            if os.path.exists(os.path.join(PATH_IMAGES, dir, name+'.npy')):
                os.remove(os.path.join(PATH_IMAGES, dir, name+'.npy'))

def deleteFullTrain(name:str):
    if os.path.exists(os.path.join(PATH_DATA_TRAIN, name + '.npy')):
        os.remove(os.path.join(PATH_DATA_TRAIN, name + '.npy'))