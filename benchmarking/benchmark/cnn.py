from settings import(
    PATH_DATA_TRAIN,
    PATH_IMAGES,
    FACE_DIM, 
    faceCascade
)
import face_recognition
import numpy as np
import os
import cv2 as cv
import glob
from sklearn.preprocessing import LabelEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm

def verifyFace(image, userID,  classifier, name="cnn"):
    featuresTest = face_recognition.face_encodings(image, num_jitters=1, model='large')
    if len(featuresTest) == 0: 
        return False, "Falha na codificação da imagem"
  
    featuresTest = featuresTest[0]

    features, _ = loadFullTrain(name)
    labels = loadFullLabels(name)

    if labels.shape[0] != features.shape[0]: return False, "caracteristicas e rotulos não coincidem"
    if features.shape[0] == 0: return False, None

    label = classifier(features, featuresTest, labels)
     
    if  label == userID: return True, None

    return False, None

def loadImage(path):
    image = cv.imread(path)
    image = cv.cvtColor(image, cv.COLOR_BGR2RGB)

    return np.asarray(image)

def loadFullTrain(trainName):
    path = PATH_DATA_TRAIN
    if os.path.exists(os.path.join(path, trainName+'.npy')):
        features = np.load(os.path.join(path, trainName + '.npy'))
        return features, None
    features = []
    errors = []  
    
    directories = os.listdir(PATH_IMAGES)
    for directorie in directories:
        if os.path.isdir(os.path.join(PATH_IMAGES, directorie)):
            featuresUser, error = train(PATH_IMAGES, directorie, trainName)
            if error is not None:
                errors += error
            if featuresUser is not None:
                features.append(featuresUser)

    if(not os.path.exists(path)):
        os.mkdir(path)
    
    features = np.array(features, dtype=float)
    np.save(os.path.join(path, trainName+'.npy'), features)
                
    return features, errors

def readAllTrains(trainName="cnn"):
    path = PATH_DATA_TRAIN
    features = []
    errors:str
    
    directories = os.listdir(PATH_IMAGES)
    for directorie in directories:
        if os.path.isdir(os.path.join(PATH_IMAGES, directorie)):
            featuresUser, error = train(PATH_IMAGES, directorie, trainName)
            if error is not None:
                errors = error
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

def updateTrain(path:str, userID:int, name):
    faces, error = extractFace(path, userID)
    if error is not None: return None, error

    for face in faces: 
        features = face_recognition.face_encodings(face, num_jitters=1, model='large')
        if len(features) != 0:
            features = features[0]
            np.save(path + '/' + str(userID) + '/' + name + '.npy', features)
            return  features, error

    return None, "Nenhuma caracteristica encontrada"


def train(path:str, userID:int, name:str):
    if os.path.exists(path+"/"+str(userID)+'/' + name + '.npy'):
        features = np.load(path+"/"+str(userID)+'/' + name + '.npy')   
        return features, None 

    return updateTrain(path, userID, name)

def extractFace(path:str, userID:int):
    images = loadUserDataset(path, userID)
    faces =[]

    for image in images:
        face, error = findFace(image)
        if error is None:
            faces.append(face)

    if len(faces) == 0:
        return None, "Nenhuma face encontrada"
    
    return faces, None

def loadUserDataset(path:str, userID:int):
    images = []

    types = ('/*.jpg', '/*.jpeg')
    pathImages = []
    for imagesType in types:
        pathImages.extend(glob.glob(path+"/"+str(userID)+imagesType))

    for pathImage in pathImages: 
        image = loadImage(pathImage)
        if image is None:
            print("Erro loaddataset, erro ao carregar imagem.")
        else:
            images.append(image)

    return images

def findFace(image):
    imageGrayScale = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    facesPositions = faceCascade.detectMultiScale(imageGrayScale)
    
    if len(facesPositions) > 0:
        column, row, width, height = facesPositions[0]
    else:
        return None, 'Erro ao localizar face, não existe faces na imagem. \n'

    for face in facesPositions:
        if height < face[3]:
            column, row, width, height = face

    cropFace = image[row: row+height, column:column+width]
    cropFace = cv.resize(cropFace, (FACE_DIM, FACE_DIM))    

    return cropFace, None


def euclidianDistance(features, featureTest, labels):
    tolerance = 0.6
    distances = np.linalg.norm(features - featureTest, axis=1)

    label = None
    bestResult = distances.argmin()
    if distances[bestResult] <= tolerance:
        label = labels[bestResult]

    return label

def knn_1(features, featureTest, labelsUser):
    k=1
    labelEncoder = LabelEncoder()
    labels = labelEncoder.fit_transform(labelsUser)

    model = KNeighborsClassifier(n_neighbors = k, n_jobs=-1)
    model.fit(features, labels)

    result = model.predict([featureTest])
    label = labelEncoder.inverse_transform(result)

    return label


def svm_linear(features, featureTest, labelsUser):
    kernel='linear'
    labelEncoder = LabelEncoder()
    labels = labelEncoder.fit_transform(labelsUser)

    model = svm.SVC(kernel=kernel)
    model.fit(features, labels)

    result = model.predict([featureTest])
    label = labelEncoder.inverse_transform(result)

    return label

def svm_no_linear(features, featureTest, labelsUser):
    labelEncoder = LabelEncoder()
    labels = labelEncoder.fit_transform(labelsUser)
    model = svm.NuSVC(gamma="auto")
    model.fit(features, labels)

    result = model.predict([featureTest])
    label = labelEncoder.inverse_transform(result)

    return label