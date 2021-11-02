from cv2 import imread
import numpy as np
import os
from recognition.findFace import extractFace
from skimage.io import imread
from skimage.feature import hog

def extractFeature(image):
    fd, hog_image = hog(image, orientations=9, pixels_per_cell=(5, 5),
                	cells_per_block=(2, 2), visualize=True, multichannel=True)

    fd, hog_image = hog(image, orientations=9, pixels_per_cell=(5, 5),
                	cells_per_block=(2, 2), visualize=True, multichannel=True)
    
    return hog_image

def train(path, userID):
    if os.path.exists(path+"/"+userID+'/hog.txt'):
        features = np.loadtxt(path+"/"+userID+'/hog.txt', float)   
        return features, None 
    
    images, error = extractFace(path, userID)

    if error is not None:
        return None, error
    
    if images[0] is None:
        return None, "Erro no treinamento, imagens nulas."

    
    dataFeatures = np.array(features, float)
    np.savetxt(path+"/"+userID+'/hog.txt', dataFeatures, fmt='%1.5f')

    return features, None

def updateTrain(path, userID):
    images, error = extractFace(path, userID)

    if error is not None:
        return error
    
    if images[0] is None:
        return None, "Erro no treinamento, imagens nulas."

    #data = covarianceMatrix(images)
    #features, _ = cv.PCACompute(data, mean=None, maxComponents=numberComponents) 
    
    dataFeatures = np.array(features, int)
    np.savetxt(path+"/"+userID+'/data.txt', dataFeatures)

    return  None

if __name__ == "__main__":
    image = imread("/static/image/eu.jpg")
    extractFeature(image)