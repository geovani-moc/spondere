from os import error
from skimage.feature import local_binary_pattern
from skimage.feature import hog
import numpy as np
import cv2 as cv
from recognition.findFace import findFace
from settings import EIGENFACES_NUMBER_COMPONENTS

def extractFeatureLBP(image):
    lbp = local_binary_pattern(image, 8,1.0,method='default')
    lbp = lbp.flatten()
    return lbp, None

#fazer a extração de todas ou de uma por vez?(image ou images)
def extractFeatureEigenFaces(image):
    #nao está com bom resultado
    data = covarianceMatrix([image])
    feature, _ = cv.PCACompute(data, mean=None, maxComponents=EIGENFACES_NUMBER_COMPONENTS) 

    #2d para 1d
    if feature.ndim == 2:
        feature = feature[0]

    return feature, None

def extractFeatureHOG(image):
    hog_image = hog(image, orientations=9, pixels_per_cell=(10, 10), cells_per_block=(1, 1))
    return hog_image, None

def covarianceMatrix(images):
    numberImages = len(images)
    shape = images[0].shape

    data = np.zeros((numberImages, shape[0]* shape[1]), dtype = np.float32)

    for number in range(0, numberImages):
        image = images[number].flatten()
        data[number,:] = image

    return data
