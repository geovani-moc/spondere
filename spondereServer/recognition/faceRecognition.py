from typing import Any
from sklearn import svm
from util.recognition import loadFullLabels, loadFullTrain
from sklearn.preprocessing import LabelEncoder
from recognition.featureExtraction import extractFeature
import settings

#svm classificador
def verifyFace(image, userID):
    name = 'hog'
    featureMethod = extractFeature
    kernel='linear'
    features = Any
    labelsUser = Any

    featuresTest = featureMethod([image])

    if len(settings.SVM_HOG) > 0:
        features = settings.SVM_HOG
    else:
        features, errors = loadFullTrain(name, featureMethod)
        #if len(errors) > 0: print(errors, file=stderr)
        settings.SVM_HOG = features

    if len(settings.LABELS) > 0:
        labelsUser = settings.LABELS
    else:
        labelsUser = loadFullLabels(name)
        settings.LABELS = labelsUser

    if len(labelsUser) != len(features): return False, "Erro: r001"
    if len(features) == 0: return False, "Erro: r002"

    labelEncoder = LabelEncoder()
    labelsUser = labelEncoder.fit_transform(labelsUser)

    featuresLettering, labels = lettering(features, labelsUser)

    model = svm.SVC(kernel=kernel)
    model.fit(featuresLettering, labels)

    result = model.predict(featuresTest)
    label = labelEncoder.inverse_transform(result)

    if label[0] == userID: return True, None

    return False, "A face do usuário não foi reconhecida."

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