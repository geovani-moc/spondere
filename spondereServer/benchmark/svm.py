from sklearn import svm
from util.recognition import loadFullLabels, loadFullTrain
from sklearn.preprocessing import LabelEncoder
from sys import stderr

def verifyFace(image, userID, featureMethod, kernel='linear'):

    featuresTest, error = featureMethod(image)
    if error is not None: return None, error

    features, errors = loadFullTrain("knn", featureMethod)
    if len(errors) > 0: print(errors, file=stderr)
    labels = loadFullLabels()

    if len(labels) != len(features): return False, "caracteristicas e rotulos não coincidem"
    if len(features) == 0: return False, None

    labelEncoder = LabelEncoder()
    labels = labelEncoder.fit_transform(labels)

    model = svm.SVC(kernel=kernel)
    model.fit(features, labels)

    result = model.predict(featuresTest)
    label = labelEncoder.inverse_transform(result)

    if label == userID: return True, None

    return False, None