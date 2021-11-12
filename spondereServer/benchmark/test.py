from recognition.findFace import extractFace
from settings import(
    PATH_IMAGES
)
import os
from benchmark import (
    knn, 
    svm, 
    euclideanDistance,
    features
)

from util.image import loadImages


def test(classifier, name, extractMethod) -> float:
    count:float = 0
    hits:float = 0 

    directories = os.listdir(PATH_IMAGES)

    for directorie in directories:
        if os.path.isdir(os.path.join(PATH_IMAGES, directorie)):
            if (os.path.exists(os.path.join(PATH_IMAGES, directorie, 'false')) and 
                os.path.exists(os.path.join(PATH_IMAGES, directorie, 'true'))):
                
                tempCount, tempHits = testImages(directorie, classifier, name, extractMethod, 'false')
                count = count + tempCount
                hits = hits + (tempCount - tempHits)

                tempCount, tempHits = testImages(directorie, classifier, name, extractMethod, 'true')
                count += tempCount
                hits += tempHits
    
    if count == 0: return 0

    return (hits/count)

def testImages(userID, classifier, name, extractMethod, folder):
    #path = os.path.join(PATH_IMAGES, userID, folder)
    images, error = extractFace(PATH_IMAGES, os.path.join(userID, folder))

    hits:float = 0
    count:float = 0
    for image in images:
        result, error = classifier(image, userID, name, extractMethod)
        if result: hits += 1
        count += 1
    
    return count, hits


if __name__ == '__main__':

    KNN = knn.verifyFace
    SVM = svm.verifyFace
    euclidean = euclideanDistance.verifyFace

    hog = features.extractFeatureHOG
    lbp = features.extractFeatureLBP
    eigen = features.extractFeatureEigenFaces

    # euclidianDistance_eigen = test(euclidean, 'eigen', eigen)
    # euclidianDistance_lbp = test(euclidean, 'lbp', lbp)
    euclidianDistance_hog = test(euclidean, 'hog', hog)
    print("Distancia euclidiana:")
    # print(" |->Eigenfaces: ", euclidianDistance_eigen)
    # print(" |->LBP: ", euclidianDistance_lbp)
    print(" |->HOG: ", euclidianDistance_hog)

    # knn_lbp = test(KNN, 'lbp', lbp)
    # knn_eigen = test(KNN, 'eigen', eigen)
    # knn_hog = test(KNN, 'hog', hog)
    # print("KNN:")
    # print(" |->Eigenfaces: ", knn_eigen)
    # print(" |->LBP: ", knn_lbp)
    # print(" |->HOG: ", knn_hog)

    # svm_lbp = test(SVM, 'lbp', lbp)
    # svm_eigen = test(SVM, 'eigen', eigen)
    # svm_hog = test(SVM, 'hog', hog)
    # print("SVM(linear):")
    # print(" |->Eigenfaces: ", svm_eigen)
    # print(" |->LBP: ", svm_lbp)
    # print(" |->HOG: ", svm_hog)

