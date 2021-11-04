from settings import (
    EIGENFACES_NUMBER_COMPONENTS,
    THRESHOLD, 
    PATH_IMAGES)
from hog import train
import cv2 as cv
import numpy as np
import os

def verifyFace(featuresTest, userID):
    features, error = train(PATH_IMAGES, userID)
    if error is not None:
        return False, error
    
    euclidianDistance = cv.norm(features - featuresTest, cv.NORM_L2)

    if euclidianDistance > THRESHOLD:
        return False, None

    return True, None



    
if __name__ == '__main__':
    pass
