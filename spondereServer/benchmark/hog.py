from cv2 import imread
import numpy as np
import os
from recognition.findFace import extractFace
from skimage.transform import resize
from skimage.io import imread
from skimage.feature import hog
from skimage.color import rgb2gray
from settings import MIN_SIZE_DATASET


def extractFeature(image):
    hog_image = hog(image, orientations=9, pixels_per_cell=(10, 10), cells_per_block=(1, 1))
    
    return hog_image

def train(path, userID):
    if os.path.exists(path+"/"+userID+'/hog.txt'):
        features = np.loadtxt(path+"/"+userID+'/hog.txt', float)   
        return features, None

    return updateTrain(path, userID)

def updateTrain(path, userID):
    images, error = extractFace(path, userID)

    if error is not None:
        return None, error
    
    if len(images) < MIN_SIZE_DATASET:
        return None, "O usuario não tem imagens sufucientes com a face detectavel."

    features = []
    for image in images:
        feature = extractFeature(image)
        features.append(feature)
    
    dataFeatures = np.array(features, float)
    np.savetxt(path+"/"+userID+'/hog.txt', dataFeatures)

    return  dataFeatures, None

if __name__ == "__main__":
    image = imread('./static/image/eu.jpg')
    image = resize(image, (50, 50))
    image = rgb2gray(image)
    extractFeature(image)