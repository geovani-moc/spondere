from util.recognition import loadFullLabels, loadFullTrain
from face_recognition import face_encodings
import numpy as np


def verifyFace(image, userID:int, name = 'cnn'):
    
    featuresTest = face_encodings(image, num_jitters=1, model='large')
    if len(featuresTest) == 0: 
        return False, "Error: r006"
    featuresTest = featuresTest[0]

    features, _ = loadFullTrain(name)
    labels = loadFullLabels(name)

    if labels.shape[0] != features.shape[0]: 
        return False, "Error: r001"
    if features.shape[0] == 0: return False, "Error: r002"

    label = euclidianDistance(features, featuresTest, labels)
     
    if  label == str(userID): return True, None

    return False, "Error: r005"

def euclidianDistance(features, featureTest, labels):
    tolerance = 0.6
    distances = np.linalg.norm(features - featureTest, axis=1)

    label = None
    bestResult = distances.argmin()
    if distances[bestResult] <= tolerance:
        label = labels[bestResult]

    return label