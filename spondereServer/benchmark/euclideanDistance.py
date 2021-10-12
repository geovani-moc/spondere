from settings import EIGENFACES_NUMBER_COMPONENTS, THRESHOLD, pathSMVTrain, PATH_IMAGES, pathDataTrain
import cv2 as cv
from recognition.findFace import findFace
import numpy as np
import os
from recognition.featureExtraction import covarianceMatrix, train

def verifyFace(trainFeature, image, numberComponents = EIGENFACES_NUMBER_COMPONENTS):
    image = cv.equalizeHist(image)
    face, error = findFace(image)
    if error is not None:
        return None, "error em localizar a face"
    
    images = []
    images.append(face)
    data = covarianceMatrix(images)
    feature, _ = cv.PCACompute(data, mean=None, maxComponents= numberComponents)
    
    #printFeature(feature, image.shape)
    euclidianDistance = cv.norm(trainFeature - feature, cv.NORM_L2)

    if euclidianDistance > THRESHOLD:
        return False, None

    return True, None

 
def createDataFeatures(path = PATH_IMAGES):
    fullPath = './'+path+'/'
    directories = os.listdir(fullPath)

    labels=[]
    dataFeatures=[]
    errors = []

    for directory in directories:
        if os.path.isdir(fullPath + directory):

            feature, error = train(path, directory)

            if error is None:
                labels.append(directory)
                dataFeatures.append(feature)
            else:
                errors.append(error)
    
    dataFeatures = np.array(dataFeatures, float)

    np.savetxt(pathDataTrain+"/feature.txt", dataFeatures, fmt='%1.5f')
    np.savetxt(pathDataTrain+"/labels.txt", labels, delimiter=" ", fmt='%s')
    
    if len(errors) == 0:
        return None

    return errors

def faceRecognition(image, features = None, labels = None):
    if (labels is None or
        features is None):
        if (not os.path.exists(pathDataTrain+'/labels.txt') and 
            not os.path.exists(pathDataTrain+'/feature.txt')):
            error = createDataFeatures(PATH_IMAGES)
            if error is not None: return None, error

        features = np.loadtxt(pathDataTrain+"/feature.txt", float)
        labels = np.loadtxt(pathDataTrain+"/labels.txt", str)
    
    result, error = verifyFace(features, labels, image, EIGENFACES_NUMBER_COMPONENTS)

    if error is not None:
        return None, error

    return result, None
    
if __name__ == '__main__':
    error = createDataFeatures()
    if error is not None:
        raise Exception(error)
    else:print('Ok')


            

