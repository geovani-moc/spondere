from skimage import feature
from database import user
from settings import(
    PATH_DATA_TRAIN,
    PATH_IMAGES,
    MIN_SIZE_DATASET, 
    NUMBER_FEATURES_DATASET
)
import os
import numpy as np
from recognition.findFace import extractFace

def loadFullTrain(trainName, method):
    path = PATH_DATA_TRAIN
    if os.path.exists(os.path.join(path, trainName+'.npy')):
        features = np.load(os.path.join(path, trainName + '.npy'))
        return features, None
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
    if os.path.exists(path + '/labels.npy'):
        labels = np.load(path+"/labels.npy")
        return labels
    
    labels = []
    directories = os.listdir(PATH_IMAGES)
    for directorie in directories:
        if os.path.isdir(os.path.join(PATH_IMAGES, directorie)):
            if os.path.exists(os.path.join(PATH_IMAGES, directorie, name+'.npy')):
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
        
        if feature is not None or len(features) > 1:
            features.append(np.array(feature, dtype=float))
    
    if len(features) < MIN_SIZE_DATASET:
        return None, "quantidade de caracteristicas insuficiente:" + userID

    features = normalizeFeatures(features)
    features = np.array(features, dtype=float)

    np.save(path + '/' + userID + '/' + name + '.npy', features)

    return  features, errors

def normalizeFeatures(features):
    if len(features) > NUMBER_FEATURES_DATASET:
        return features[0:NUMBER_FEATURES_DATASET]

    if len(features) < NUMBER_FEATURES_DATASET:
        for i in range(len(features), NUMBER_FEATURES_DATASET):
            features = np.concatenate((features, [features[0]])) #checar se fetures tem size = numeber features dataset

    return features

def train(path, userID, method, name="eigen"):

    if os.path.exists(path+"/"+userID+'/' + name + '.npy'):
        features = np.load(path+"/"+userID+'/' + name + '.npy')   
        return features, None 

    return updateTrain(path, userID, method, name)

def deleteTrain(name):
    dirs = os.listdir(PATH_IMAGES)
    for dir in dirs:
        if os.path.isdir(os.path.join(PATH_IMAGES, dir)):
            if os.path.exists(os.path.join(PATH_IMAGES, dir, name+'.npy')):
                os.remove(os.path.join(PATH_IMAGES, dir, name+'.npy'))

def deleteFullTrain(name):
    if os.path.exists(os.path.join(PATH_DATA_TRAIN, name + '.npy')):
        os.remove(os.path.join(PATH_DATA_TRAIN, name + '.npy'))