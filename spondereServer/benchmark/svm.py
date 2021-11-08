from sklearn import svm
from util.recognition import loadFullLabels, loadFullTrain
from sklearn.preprocessing import LabelEncoder

def verifyFace(featuresTest, userID, featureMethod, kernel='linear'):

    features = loadFullTrain("knn", featureMethod)
    labels = loadFullLabels()

    labelEncoder = LabelEncoder()
    labels = labelEncoder.fit_transform(labels)

    model = svm.SVC(kernel=kernel)
    model.fit(features, labels)

    result = model.predict(featuresTest)
    label = labelEncoder.inverse_transform(result)

    if label == userID: return True

    return False