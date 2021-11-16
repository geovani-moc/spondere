from os import error
from skimage.feature import local_binary_pattern
from skimage.feature import hog
import numpy as np
import cv2 as cv
from recognition.findFace import extractFace
from settings import EIGENFACES_NUMBER_COMPONENTS, FACE_DIM, PATH_IMAGES
from util.image import printFeature


def extractFeatureLBP(images):
    #analisar a extração de caracteristicas do lbp
    features = []
    for image in images:
        lbp = local_binary_pattern(image, 8,1.0,method='default')
        features.append(lbp.flatten())

    return np.array(features, dtype=float)

def extractFeatureEigenFaces(images):
    
    data = covarianceMatrix(images)
    features, _ = cv.PCACompute(data, mean=None, maxComponents=EIGENFACES_NUMBER_COMPONENTS) 

    # if features.ndim == 2:
    #    features = features[0]

    return np.array(features, dtype=float)

def extractFeatureHOG(images):
    features = []
    for image in images:
        features.append(hog(image, orientations=9, pixels_per_cell=(10, 10), cells_per_block=(1, 1)))

    return np.array(features, dtype=float)

def covarianceMatrix(images):
    numberImages = len(images)
    shape = images[0].shape

    data = np.zeros((numberImages, shape[0]* shape[1]), dtype = np.float32)

    for number in range(0, numberImages):
        image = images[number].flatten()
        data[number,:] = image

    return data

if __name__ == '__main__':
    faces, error = extractFace(PATH_IMAGES, 's01')

    feature, error = extractFeatureEigenFaces(faces)
    printFeature(feature, FACE_DIM)