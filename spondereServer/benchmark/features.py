from skimage.feature import local_binary_pattern
from skimage.feature import hog
from skimage.transform import resize
from skimage.io import imread
from skimage.color import rgb2gray
import numpy as np
import cv2 as cv
from settings import EIGENFACES_NUMBER_COMPONENTS

def extractFeatureLBP(image):
    lbp = local_binary_pattern(image, 8,1.0,method='default')
    return lbp

#fazer a extração de todas ou de uma por vez?(image ou images)
def extractFeatureEigenFaces(images):
    data = covarianceMatrix(images)
    features, _ = cv.PCACompute(data, mean=None, maxComponents=EIGENFACES_NUMBER_COMPONENTS) 

    if features.ndim == 2:
        features = features[0]

    return features

def extractFeatureHOG(image):
    hog_image = hog(image, orientations=9, pixels_per_cell=(10, 10), cells_per_block=(1, 1))
    return hog_image

def covarianceMatrix(images):
    numberImages = len(images)
    shape = images[0].shape

    data = np.zeros((numberImages, shape[0]* shape[1]), dtype = np.float32)

    for number in range(0, numberImages):
        image = images[number].flatten()
        data[number,:] = image

    return data

if __name__ == "__main__":
    image = imread('./static/image/eu.jpg')
    image = resize(image, (50, 50))
    image = rgb2gray(image)
    extractFeatureHOG(image)