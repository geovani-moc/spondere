import cv2 as cv
from settings import (
    PATH_DATA_TRAIN,
    PATH_IMAGES
)
import os
import numpy as np


def verifyFace(trainFeatures, labels, featuresTest, k = 1):
    #knn = cv.ml_KNearest()
    knn = cv.ml.KNearest_create()
    knn.train(trainFeatures, labels)
    ret, results, neighbours, dist = knn.findNearest(featuresTest, k)

    print ("results: ", results,"\n")
    print ("neighbours: ", neighbours,"\n")
    print ("distances: ", dist)


if __name__ == '__main__':

    if (os.path.exists(PATH_DATA_TRAIN + '/labels.txt') and 
            not os.path.exists(PATH_DATA_TRAIN + '/feature.txt')):
        features = np.loadtxt(PATH_DATA_TRAIN + "/feature.txt", float)
        labels = np.loadtxt(PATH_DATA_TRAIN + "/labels.txt", str)

        #fazer a estraçao de caracteristidas de uma imagem para testar
        featuresTest = []

        verifyFace(features, labels, featuresTest)
