from settings import (
    PATH_DATA_TRAIN,
    NUMBER_NEIGHBORS
)
import os
import numpy as np
from util.recognition import loadFullLabels, loadFullTrain
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder


# a entrada que representa as caracteristicas da face deve ser um vetor unidimensional
def verifyFace(featuresTest, userID, featureMethod):
    #otmizar na versão final, deixar tudo em memoria
    features = loadFullTrain("knn", featureMethod)
    labels = loadFullLabels()

    labelEncoder = LabelEncoder()
    labels = labelEncoder.fit_transform(labels)

    model = KNeighborsClassifier(n_neighbors= NUMBER_NEIGHBORS, n_jobs=-1)
    model.fit(features, labels)

    result = model.predict(featuresTest)
    label = labelEncoder.inverse_transform(result)

    if label == userID: return True

    return False


if __name__ == '__main__':

    if (os.path.exists(PATH_DATA_TRAIN + '/labels.txt') and 
            not os.path.exists(PATH_DATA_TRAIN + '/feature.txt')):
        features = np.loadtxt(PATH_DATA_TRAIN + "/feature.txt", float)
        labels = np.loadtxt(PATH_DATA_TRAIN + "/labels.txt", str)

        #fazer a estraçao de caracteristidas de uma imagem para testar
        featuresTest = []

        verifyFace(features, labels, featuresTest)
