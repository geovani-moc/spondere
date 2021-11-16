from settings import (
    PATH_DATA_TRAIN,
    NUMBER_NEIGHBORS
)
import os
import numpy as np
from util.recognition import loadFullLabels, loadFullTrain
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder
from sys import stderr

def verifyFace(image, userID, name, featureMethod):

    featuresTest = featureMethod([image])

    features, errors = loadFullTrain(name, featureMethod)
    #if len(errors) > 0: print(errors, file=stderr)
    labelsUser = loadFullLabels(name)

    if len(labelsUser) != len(features): return False, "caracteristicas e rotulos não coincidem"
    if len(features) == 0: return False, None

    labelEncoder = LabelEncoder()
    labelsUser = labelEncoder.fit_transform(labelsUser)

    featuresLettering, labels = lettering(features, labelsUser)

    k = NUMBER_NEIGHBORS
    if name == 'eigen':
        k = 1
    
    model = KNeighborsClassifier(n_neighbors = k, n_jobs=-1)
    model.fit(featuresLettering, labels)

    result = model.predict(featuresTest)
    label = labelEncoder.inverse_transform(result)

    if label[0] == userID: return True, None

    return False, None

def lettering(features, labelsUser):
    count = 0
    labels = []
    featuresLettering = []

    for featuresUser in features:
        label = labelsUser[count]
        for feature in featuresUser:
            featuresLettering.append(feature)
            labels.append(label)
        count += 1  
    
    featuresLettering = np.array(featuresLettering, dtype=float)

    return featuresLettering, labels

if __name__ == '__main__':

    if (os.path.exists(PATH_DATA_TRAIN + '/labels.npy') and 
            not os.path.exists(PATH_DATA_TRAIN + '/feature.npy')):
        features = np.load(PATH_DATA_TRAIN + "/feature.npy")
        labels = np.load(PATH_DATA_TRAIN + "/labels.npy")

        #fazer a estraçao de caracteristidas de uma imagem para testar
        featuresTest = []

        verifyFace(features, labels, featuresTest)
