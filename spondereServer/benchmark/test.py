from recognition.findFace import extractFace
from settings import(
    PATH_IMAGES
)
import os
from benchmark import (
    knn, 
    svm, 
    euclideanDistance,
    features,
    svm_nonLinear
)



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
    faces, error = extractFace(PATH_IMAGES, os.path.join(userID, folder))

    hits:float = 0
    count:float = 0
    for face in faces:
        result, error = classifier(face, userID, name, extractMethod)
        if result: hits += 1
        count += 1
    
    return count, hits


if __name__ == '__main__':

    KNN = knn.verifyFace
    SVM = svm.verifyFace
    euclidean = euclideanDistance.verifyFace
    SVM_nonLinear = svm_nonLinear.verifyFace

    hog = features.extractFeatureHOG
    lbp = features.extractFeatureLBP
    eigen = features.extractFeatureEigenFaces

    print("Distancia euclidiana:")
    # euclidianDistance_eigen = test(euclidean, 'eigen', eigen) #50%
    # print(" |->Eigenfaces: ", euclidianDistance_eigen)
    # euclidianDistance_lbp = test(euclidean, 'lbp', lbp) #68%
    # print(" |->LBP: ", euclidianDistance_lbp)
    euclidianDistance_hog = test(euclidean, 'hog', hog) #76% ori=9, 77% ori=15, 83% ori=15 5x5 2x2, 82% ori=15 5x5 1x1, 
    print(" |->HOG: ", euclidianDistance_hog)

    print("KNN:")
    # knn_lbp = test(KNN, 'lbp', lbp) #76% k=5, 76% k=3, 75% k=7, 78% k=1
    # print(" |->LBP: ", knn_lbp)
    # knn_eigen = test(KNN, 'eigen', eigen) #50% k=1
    # print(" |->Eigenfaces: ", knn_eigen)
    knn_hog = test(KNN, 'hog', hog) #79% k=5, 81% k=3 ori=9, 78% k=7, 84% k=1, 86% k=3 ori=15, 89% ori=15 5x5 2x2, 88% ori=15 5x5 1x1,
    print(" |->HOG: ", knn_hog)

    print("SVM(linear):")
    # svm_lbp = test(SVM, 'lbp', lbp) #85%
    # print(" |->LBP: ", svm_lbp)
    # svm_eigen = test(SVM, 'eigen', eigen) #50%
    # print(" |->Eigenfaces: ", svm_eigen)
    svm_hog = test(SVM, 'hog', hog) #85% ori=9, 86% ori=15, 91% ori=15 5x5 2x2, 88% ori=15 5x5 1x1,
    print(" |->HOG: ", svm_hog)

    print("SVM(não linear)")
    # svmNonLinear_lbp = test(SVM_nonLinear, 'lbp', lbp) #51%
    # print(" |->LBP: ", svmNonLinear_lbp)
    # svmNonLinear_eigen = test(SVM_nonLinear, 'eigen', eigen) #50%
    # print(" |->Eigenfaces: ", svmNonLinear_eigen)
    svmNonLinear_hog = test(SVM_nonLinear, 'hog', hog) #84% ori=9, 86% ori=15, , 91% ori=15 5x5 2x2, 88% ori=15 5x5 1x1,
    print(" |->HOG: ", svmNonLinear_hog)
