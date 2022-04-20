import numpy as np
from util.recognition import(
    loadFullLabels,
    loadFullTrain
)


def verifyFace(image, userID, name, featureMethod, args):
    
    featuresTest = featureMethod([image], args)
    if featuresTest is None: return None, "Erro na geração de caracteristicas. " + name

    features, _ = loadFullTrain(name, featureMethod, args)
    labels = loadFullLabels(name)

    if len(labels) != features.shape[0]: return False, "caracteristicas e rotulos não coincidem"
    if len(features) == 0: return False, None

    bestLabel:str = labels[0]
    bestFeature:float =  euclidianDistance(features[0], featuresTest[0])

    count = 0
    for feature in features:
        distance = euclidianDistance(feature, featuresTest[0])
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
    
