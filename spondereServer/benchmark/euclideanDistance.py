from settings import (
    EIGENFACES_NUMBER_COMPONENTS,
    THRESHOLD, 
    PATH_IMAGES)
import cv2 as cv
import numpy as np
import os

def verifyFace(trainFeature, labels, userID, featuresTest):
    feature = []
    count:int = 0
    for label in labels:
        if label == userID:
            feature = trainFeature[count]
            break
        count = count + 1
    
    euclidianDistance = cv.norm(feature - featuresTest, cv.NORM_L2)

    if euclidianDistance > THRESHOLD:
        return False, None

    return True, None



    
if __name__ == '__main__':
    pass


            

