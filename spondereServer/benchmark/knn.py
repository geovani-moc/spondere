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
def verifyFace(image, userID, featureMethod):
    #otmizar na versão final, deixar tudo em memoria

    featuresTest, error = featureMethod(image)
    if error is not None: return None, error

    features, errors = loadFullTrain("knn", featureMethod)
    if len(errors) > 0: print(errors, file=stderr)
    labels = loadFullLabels()

    if len(labels) != len(features): return False, "caracteristicas e rotulos não coincidem"
    if len(features) == 0: return False, None

    labelEncoder = LabelEncoder()
    labels = labelEncoder.fit_transform(labels)

    model = KNeighborsClassifier(n_neighbors= NUMBER_NEIGHBORS, n_jobs=-1)
    model.fit(features, labels)

    result = model.predict(featuresTest)
    label = labelEncoder.inverse_transform(result)

    if label == userID: return True, None

    return False, None


if __name__ == '__main__':

    if (os.path.exists(PATH_DATA_TRAIN + '/labels.txt') and 
            not os.path.exists(PATH_DATA_TRAIN + '/feature.txt')):
        features = np.load(PATH_DATA_TRAIN + "/feature.txt")
        labels = np.load(PATH_DATA_TRAIN + "/labels.txt")

        #fazer a estraçao de caracteristidas de uma imagem para testar
        featuresTest = []

        verifyFace(features, labels, featuresTest)
