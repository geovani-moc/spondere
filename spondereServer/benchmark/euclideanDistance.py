import numpy as np
from util.recognition import(
    loadFullLabels,
    loadFullTrain
)
from sys import stderr

def verifyFace(image, userID, name, featureMethod):
    featuresTest, error = featureMethod(image)
    if error is not None: return None, error

    features, errors = loadFullTrain(name, featureMethod)
    #if len(errors) > 0: print(errors, file=stderr)#imagens com face nao localizadas
    labels = loadFullLabels(name)

    if len(labels) != len(features): return False, "caracteristicas e rotulos não coincidem"
    if len(features) == 0: return False, None

    bestLabel:str = labels[0]
    bestFeature:float =  euclidianDistance(features[0], featuresTest)

    count = 1
    for feature in features:
        distance = euclidianDistance(feature, featuresTest)
        if bestFeature > distance:
            bestFeature = distance
            bestLabel = labels[count]
        count = count + 1

    if bestLabel == userID:
        return True, None

    return False, None

def euclidianDistance(features, test) -> float:
    if len(features) == 0: return 0

    result = 0
    for feature in features:
        result += np.linalg.norm(feature - test)

    return result / len(features)
    
if __name__ == '__main__':
    pass

