import numpy as np
from util.recognition import(
    loadFullLabels,
    loadFullTrain
)
from sys import stderr

def verifyFace(image, userID, featureMethod):
    featuresTest, error = featureMethod(image)
    if error is not None: return None, error

    features, errors = loadFullTrain("euclidean_distance", featureMethod)
    if len(errors) > 0: print(errors, file=stderr)
    labels = loadFullLabels()

    if len(labels) != len(features): return False, "caracteristicas e rotulos não coincidem"
    if len(features) == 0: return False, None

    bestLabel:str = labels[0]
    bestFeature:float =  np.linalg.norm(features[0] - featuresTest)

    count = 1
    for feature in features:
        euclidianDistance =  np.linalg.norm(feature - featuresTest)
        if bestFeature > euclidianDistance:
            bestFeature = euclidianDistance
            bestLabel = labels[count]
        count = count + 1

    if bestLabel == userID:
        return True, None

    return False, None
    
if __name__ == '__main__':
    pass
