from util.recognition import loadFullLabels, loadFullTrain
from sklearn.preprocessing import LabelEncoder

def verifyFace(image, userID, name, featureMethod, args):
    kernel='linear'
    featuresTest = featureMethod([image], args)

    features, _ = loadFullTrain(name, featureMethod, args)
    labelsUser = loadFullLabels(name)

    if len(labelsUser) != len(features): return False, "caracteristicas e rotulos não coincidem"
    if len(features) == 0: return False, None

    labelEncoder = LabelEncoder()
    labelsUser = labelEncoder.fit_transform(labelsUser)

    featuresLettering, labels = lettering(features, labelsUser)

    ##classificador
    model = svm.SVC(kernel=kernel)
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

    return featuresLettering, labels