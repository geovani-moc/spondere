import cv2 as cv
from settings import (
    PATH_DATA_TRAIN,
    PATH_IMAGES
)
import os
import numpy as np
from util.recognition import loadFullTrain
from benchmark.features import (
    extractFeatureLBP,
    extractFeatureHOG,
    extractFeatureEigenFaces
)


def verifyFace(featuresTest, userID, featureMethod):
    features = loadFullTrain("knn", featureMethod)
    #implementaçao do KNN


if __name__ == '__main__':

    if (os.path.exists(PATH_DATA_TRAIN + '/labels.txt') and 
            not os.path.exists(PATH_DATA_TRAIN + '/feature.txt')):
        features = np.loadtxt(PATH_DATA_TRAIN + "/feature.txt", float)
        labels = np.loadtxt(PATH_DATA_TRAIN + "/labels.txt", str)

        #fazer a estraçao de caracteristidas de uma imagem para testar
        featuresTest = []

        verifyFace(features, labels, featuresTest)
