import numpy as np
from util.recognition import loadFullLabels, loadFullTrain
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import LabelEncoder

def verifyFace(image, userID, name, featureMethod, args):

    featuresTest = featureMethod([image], args)

    features, _ = loadFullTrain(name, featureMethod, args)
    labelsUser = loadFullLabels(name)

    if len(labelsUser) != len(features): return False, "caracteristicas e rotulos não coincidem"
    if len(features) == 0: return False, None

    labelEncoder = LabelEncoder()
    labelsUser = labelEncoder.fit_transform(labelsUser)

    featuresLettering, labels = lettering(features, labelsUser)

    k = args[0]
    
    model = KNeighborsClassifier(n_neighbors = k, n_jobs=-1)
    model.fit(featuresLettering, labels)

    result = model.predict(featuresTest)
    label = labelEncoder.inverse_transform(result)

    if label[0] == userID: return True, None

    return False, None

def lettering(features, labelsUser):
    count = 0
    labels = []
    featuresLettering = []

    for featuresUser in features:
        label = labelsUser[count]
        for feature in featuresUser:
            featuresLettering.append(feature)
            labels.append(label)
        count += 1  
    
    featuresLettering = np.array(featuresLettering, dtype=float)

    return featuresLettering, labels
