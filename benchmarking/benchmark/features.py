from skimage.feature import local_binary_pattern
from skimage.feature import hog
import numpy as np
import cv2 as cv
from settings import EIGENFACES_NUMBER_COMPONENTS
 

def extractFeatureLBP(images, args):
    features = []
    for image in images:
        lbp = local_binary_pattern(image, 8,1.0,method='default')
        features.append(lbp.flatten())

    return np.array(features, dtype=float)

def extractFeatureEigenFaces(images, args):
    
    data = covarianceMatrix(images)
    features, _ = cv.PCACompute(data, mean=None, maxComponents=EIGENFACES_NUMBER_COMPONENTS) 

    # if features.ndim == 2:
    #    features = features[0]

    return np.array(features, dtype=float)

def extractFeatureHOG(images, args):
    features = []
    orientations= args[1]
    pixelsPerCell= args[2]
    cellsPerBlock= args[3]

    for image in images:
        #hogImage = hog(image, orientations=9, pixels_per_cell=(10, 10), cells_per_block=(1, 1))
        #hogImage = hog(image, orientations=15, pixels_per_cell=(10, 10), cells_per_block=(1, 1))
        #hogImage = hog(image, orientations=15, pixels_per_cell=(5, 5), cells_per_block=(2, 2))
        #hogImage = hog(image, orientations=15, pixels_per_cell=(5, 5), cells_per_block=(1, 1))
        
        hogImage = hog(image, 
        orientations=orientations, 
        pixels_per_cell=pixelsPerCell, 
        cells_per_block=cellsPerBlock)

        features.append(hogImage)

    return np.array(features, dtype=float)

def covarianceMatrix(images):
    numberImages = len(images)
    shape = images[0].shape

    data = np.zeros((numberImages, shape[0]* shape[1]), dtype = np.float32)

    for number in range(0, numberImages):
        image = images[number].flatten()
        data[number,:] = image

    return data
