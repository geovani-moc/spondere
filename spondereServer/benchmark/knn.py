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


# a entrada que representa as caracteristicas da face deve ser um vetor unidimensional
def verifyFace(image, userID, name, featureMethod):
    #otmizar na versão final, deixar tudo em memoria

    featuresTest, error = featureMethod(image)
    if error is not None: return None, error

    features, errors = loadFullTrain(name, featureMethod)
    #if len(errors) > 0: print(errors, file=stderr)
    labelsUser = loadFullLabels(name)

    if len(labelsUser) != len(features): return False, "caracteristicas e rotulos não coincidem"
    if len(features) == 0: return False, None

    labelEncoder = LabelEncoder()
    labelsUser = labelEncoder.fit_transform(labelsUser)

    featuresLettering, labels = lettering(features, labelsUser)

    model = KNeighborsClassifier(n_neighbors= NUMBER_NEIGHBORS, n_jobs=-1)
    model.fit(featuresLettering, labels)#Exception has occurred: ValueError       
    #(note: full exception trace is shown but execution is paused at: <module>)
    #Expected 2D array, got 1D array instead:

    result = model.predict(featuresTest)
    label = labelEncoder.inverse_transform(result)

    if label == userID: return True, None

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
