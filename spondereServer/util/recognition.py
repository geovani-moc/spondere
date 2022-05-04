from settings import(
    PATH_DATA_TRAIN,
    PATH_IMAGES,
    MIN_SIZE_DATASET
)
import os
import numpy as np
from recognition.findFace import extractFace
from face_recognition import face_encodings

def loadFullTrain(trainName:str):
    path = PATH_DATA_TRAIN
    if os.path.exists(os.path.join(path, trainName+'.npy')):
        features = np.load(os.path.join(path, trainName + '.npy'))
        return features, None
    
    return readAllTrains(trainName)

def readAllTrains(trainName:str):
    path = PATH_DATA_TRAIN
    features = []
    errors = []  
    
    directories = os.listdir(PATH_IMAGES)
    for directorie in directories:
        if os.path.isdir(os.path.join(PATH_IMAGES, directorie)):
            feature, error = train(PATH_IMAGES, directorie, trainName)
            if error is not None:
                errors += error
            if feature is not None:
                features.append(feature)

    if(not os.path.exists(path)):
        os.mkdir(path)
    
    features = np.array(features, dtype=float)
    np.save(os.path.join(path, trainName+'.npy'), features)
                
    return features, errors

def loadFullLabels(name:str):
    path = PATH_DATA_TRAIN
    if os.path.exists(os.path.join(path, 'labels.npy')):
        labels = np.load(os.path.join(path, 'labels.npy'))
        return labels
    
    return readAllLabels(name)

def readAllLabels(name:str):
    path = PATH_DATA_TRAIN   
    labels = []
    directories = os.listdir(PATH_IMAGES)
    for directorie in directories:
        if os.path.isdir(os.path.join(PATH_IMAGES, directorie)):
            if os.path.exists(os.path.join(PATH_IMAGES, directorie, name+'.npy')):
                labels.append(directorie)
    
    labels = np.asarray(labels)
    np.save(os.path.join(path, 'labels.npy'), labels)
    
    return labels

def updateTrain(path:str, userID:int, name:str):
    faces, error = extractFace(path, userID)

    if error is not None: return None, error
    if len(faces) < MIN_SIZE_DATASET:
        return None, "r003"

    for face in faces: 
        feature = face_encodings(face, num_jitters=1, model='large')
        if len(feature) != 0:
            feature = feature[0]
            np.save(path + '/' + str(userID) + '/' + name + '.npy', feature)
            return  feature, None

    return None, "r002"

def train(path:str, userID:int, name:str):
    if os.path.exists(path+"/"+str(userID)+'/' + name + '.npy'):
        features = np.load(path+"/"+str(userID)+'/' + name + '.npy')   
        return features, None 

    return updateTrain(path, userID, name)

def deleteTrain(name:str):
    if os.path.exists(os.path.join(PATH_DATA_TRAIN, 'labels.npy')):
        os.remove(os.path.join(PATH_DATA_TRAIN, 'labels.npy'))

    if os.path.exists(os.path.join(PATH_DATA_TRAIN, name + '.npy')):
        os.remove(os.path.join(PATH_DATA_TRAIN, name + '.npy'))

    dirs = os.listdir(PATH_IMAGES)
    for dir in dirs:
        if os.path.isdir(os.path.join(PATH_IMAGES, dir)):
            if os.path.exists(os.path.join(PATH_IMAGES, dir, name+'.npy')):
                os.remove(os.path.join(PATH_IMAGES, dir, name+'.npy'))
