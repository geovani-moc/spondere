from sklearn import svm
from util.recognition import loadFullLabels, loadFullTrain
from sklearn.preprocessing import LabelEncoder
from sys import stderr

def verifyFace(image, userID, name, featureMethod, kernel='linear'):

    featuresTest, error = featureMethod(image)
    if error is not None: return None, error

    features, errors = loadFullTrain(name, featureMethod)
    #if len(errors) > 0: print(errors, file=stderr)
    labelsUser = loadFullLabels(name)

    if len(labelsUser) != len(features): return False, "caracteristicas e rotulos não coincidem"
    if len(features) == 0: return False, None

    labelEncoder = LabelEncoder()
    labelsUser = labelEncoder.fit_transform(labelsUser)

    featuresLettering, labels = lettering(features, labelsUser)

    model = svm.SVC(kernel=kernel)
    model.fit(featuresLettering, labels)

    result = model.predict(featuresTest)
    label = labelEncoder.inverse_transform(result)

    if label == userID: return True, None

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

    return featuresLettering, labels