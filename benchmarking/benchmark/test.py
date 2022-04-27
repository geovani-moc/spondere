from recognition.findFace import extractFace
from settings import(PATH_IMAGES)
import os
import glob
from benchmark import (
    knn, 
    svm, 
    euclideanDistance,
    features,
    svm_nonLinear
)
from util.recognition import deleteFullTrain, deleteTrain

def test(classifier, name, extractMethod, *args) -> float:
    count:float = 0
    hits:float = 0 

    directories = os.listdir(PATH_IMAGES)

    for directorie in directories:
        if os.path.isdir(os.path.join(PATH_IMAGES, directorie)):
            if (os.path.exists(os.path.join(PATH_IMAGES, directorie, 'false')) and 
                os.path.exists(os.path.join(PATH_IMAGES, directorie, 'true'))):
                
                tempCount, tempHits = testImages(directorie, classifier, name, extractMethod, 'false', args)
                count = count + tempCount
                hits = hits + (tempCount - tempHits)

                tempCount, tempHits = testImages(directorie, classifier, name, extractMethod, 'true', args)
                count += tempCount
                hits += tempHits
        #break
    
    if count == 0: return 0

    return (hits/count)

def testImages(userID, classifier, name, extractMethod, folder, args):
    #path = os.path.join(PATH_IMAGES, userID, folder)
    faces, _ = extractFace(PATH_IMAGES, os.path.join(userID, folder))

    hits:float = 0
    for face in faces:
        result, _ = classifier(face, userID, name, extractMethod, args)
        if result: hits += 1
        
    path = PATH_IMAGES + "/" + str(userID) + "/" + folder
    count:float =  float(len(glob.glob1(path,"*.jpg")))
    return count, hits


def beginTests():
    KNN = knn.verifyFace
    SVM = svm.verifyFace
    euclidean = euclideanDistance.verifyFace
    SVM_nonLinear = svm_nonLinear.verifyFace

    hog = features.extractFeatureHOG
    lbp = features.extractFeatureLBP
    eigen = features.extractFeatureEigenFaces
    
    print("Distancia euclidiana:")
    euclidianDistance_eigen = test(euclidean, 'eigen', eigen)
    print(" |->Eigenfaces: ", euclidianDistance_eigen)
    euclidianDistance_lbp = test(euclidean, 'lbp', lbp)
    print(" |->LBP: ", euclidianDistance_lbp)
    deleteTrain("hog")
    deleteFullTrain("hog")
    euclidianDistance_hog = test(euclidean, 'hog', hog, 1, 9, (10,10), (1,1))
    print(" |->HOG orientations=9, pixels_per_cell=(10, 10), cells_per_block=(1, 1):", euclidianDistance_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    euclidianDistance_hog = test(euclidean, 'hog', hog, 1, 15, (10,10), (1,1))
    print(" |->HOG orientations=15, pixels_per_cell=(10, 10), cells_per_block=(1, 1):", euclidianDistance_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    euclidianDistance_hog = test(euclidean, 'hog', hog, 1, 15, (5,5), (1,1))
    print(" |->HOG orientations=15, pixels_per_cell=(5, 5), cells_per_block=(1, 1):", euclidianDistance_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    euclidianDistance_hog = test(euclidean, 'hog', hog, 1, 15, (5,5), (2,2))
    print(" |->HOG orientations=15, pixels_per_cell=(5, 5), cells_per_block=(2, 2):", euclidianDistance_hog)

    print("\n\nKNN - k=1:")
    knn_lbp = test(KNN, 'lbp', lbp, 1) 
    print(" |->LBP: ", knn_lbp)
    knn_eigen = test(KNN, 'eigen', eigen, 1)
    print(" |->Eigenfaces: ", knn_eigen)
    deleteTrain("hog")
    deleteFullTrain("hog")
    knn_hog = test(KNN, 'hog', hog, 1, 9, (10,10), (1,1)) 
    print(" |->HOG orientations=9, pixels_per_cell=(10, 10), cells_per_block=(1, 1):", knn_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    knn_hog = test(KNN, 'hog', hog, 1, 15, (10,10), (1,1)) 
    print(" |->HOG orientations=15, pixels_per_cell=(10, 10), cells_per_block=(1, 1):", knn_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    knn_hog = test(KNN, 'hog', hog, 1, 15, (5,5), (1,1)) 
    print(" |->HOG orientations=15, pixels_per_cell=(5, 5), cells_per_block=(1, 1):", knn_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    knn_hog = test(KNN, 'hog', hog, 1, 15, (5,5), (2,2)) 
    print(" |->HOG orientations=15, pixels_per_cell=(5, 5), cells_per_block=(2, 2):", knn_hog)

    print("\n\nKNN - k=3:")
    knn_lbp = test(KNN, 'lbp', lbp, 3) 
    print(" |->LBP: ", knn_lbp)
    deleteTrain("hog")
    deleteFullTrain("hog")
    knn_hog = test(KNN, 'hog', hog, 3, 9, (10,10), (1,1)) 
    print(" |->HOG orientations=9, pixels_per_cell=(10, 10), cells_per_block=(1, 1):", knn_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    knn_hog = test(KNN, 'hog', hog, 3, 15, (10,10), (1,1)) 
    print(" |->HOG orientations=15, pixels_per_cell=(10, 10), cells_per_block=(1, 1):", knn_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    knn_hog = test(KNN, 'hog', hog, 3, 15, (5,5), (1,1)) 
    print(" |->HOG orientations=15, pixels_per_cell=(5, 5), cells_per_block=(1, 1):", knn_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    knn_hog = test(KNN, 'hog', hog, 3, 15, (5,5), (2,2)) 
    print(" |->HOG orientations=15, pixels_per_cell=(5, 5), cells_per_block=(2, 2):", knn_hog)

    print("\n\nKNN - k=5:")
    knn_lbp = test(KNN, 'lbp', lbp, 5) 
    print(" |->LBP: ", knn_lbp)
    deleteTrain("hog")
    deleteFullTrain("hog")
    knn_hog = test(KNN, 'hog', hog, 5, 9, (10,10), (1,1)) 
    print(" |->HOG orientations=9, pixels_per_cell=(10, 10), cells_per_block=(1, 1):", knn_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    knn_hog = test(KNN, 'hog', hog, 5, 15, (10,10), (1,1)) 
    print(" |->HOG orientations=15, pixels_per_cell=(10, 10), cells_per_block=(1, 1):", knn_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    knn_hog = test(KNN, 'hog', hog, 5, 15, (5,5), (1,1)) 
    print(" |->HOG orientations=15, pixels_per_cell=(5, 5), cells_per_block=(1, 1):", knn_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    knn_hog = test(KNN, 'hog', hog, 5, 15, (5,5), (2,2)) 
    print(" |->HOG orientations=15, pixels_per_cell=(5, 5), cells_per_block=(2, 2):", knn_hog)

    print("\n\nKNN - k=7:")
    knn_lbp = test(KNN, 'lbp', lbp, 7) 
    print(" |->LBP: ", knn_lbp)
    deleteTrain("hog")
    deleteFullTrain("hog")
    knn_hog = test(KNN, 'hog', hog, 7, 9, (10,10), (1,1)) 
    print(" |->HOG orientations=9, pixels_per_cell=(10, 10), cells_per_block=(1, 1):", knn_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    knn_hog = test(KNN, 'hog', hog,7, 15, (10,10), (1,1)) 
    print(" |->HOG orientations=15, pixels_per_cell=(10, 10), cells_per_block=(1, 1):", knn_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    knn_hog = test(KNN, 'hog', hog,7, 15, (5,5), (1,1)) 
    print(" |->HOG orientations=15, pixels_per_cell=(5, 5), cells_per_block=(1, 1):", knn_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    knn_hog = test(KNN, 'hog', hog,7, 15, (5,5), (2,2)) 
    print(" |->HOG orientations=15, pixels_per_cell=(5, 5), cells_per_block=(2, 2):", knn_hog)

    print("\n\nSVM(linear):")
    svm_lbp = test(SVM, 'lbp', lbp)
    print(" |->LBP: ", svm_lbp)
    svm_eigen = test(SVM, 'eigen', eigen)
    print(" |->Eigenfaces: ", svm_eigen)
    deleteTrain("hog")
    deleteFullTrain("hog")
    svm_hog = test(SVM, 'hog', hog, 1, 9, (10,10), (1,1)) 
    print(" |->HOG orientations=9, pixels_per_cell=(10, 10), cells_per_block=(1, 1):", svm_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    svm_hog = test(SVM, 'hog', hog, 1, 15, (10,10), (1,1)) 
    print(" |->HOG orientations=15, pixels_per_cell=(10, 10), cells_per_block=(1, 1):", svm_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    svm_hog = test(SVM, 'hog', hog, 1, 15, (5,5), (1,1))
    print(" |->HOG orientations=15, pixels_per_cell=(5, 5), cells_per_block=(1, 1):", svm_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    svm_hog = test(SVM, 'hog', hog, 1, 15, (5,5), (2,2)) 
    print(" |->HOG orientations=15, pixels_per_cell=(5, 5), cells_per_block=(2, 2):", svm_hog)

    print("\n\nSVM(não linear)")
    svmNonLinear_lbp = test(SVM_nonLinear, 'lbp', lbp) 
    print(" |->LBP: ", svmNonLinear_lbp)
    svmNonLinear_eigen = test(SVM_nonLinear, 'eigen', eigen) 
    print(" |->Eigenfaces: ", svmNonLinear_eigen)
    deleteTrain("hog")
    deleteFullTrain("hog")
    svmNonLinear_hog = test(SVM_nonLinear, 'hog', hog, 1, 9, (10,10), (1,1))
    print(" |->HOG orientations=9, pixels_per_cell=(10, 10), cells_per_block=(1, 1):", svmNonLinear_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    svmNonLinear_hog = test(SVM_nonLinear, 'hog', hog, 1, 15, (10,10), (1,1))
    print(" |->HOG orientations=15, pixels_per_cell=(10, 10), cells_per_block=(1, 1):", svmNonLinear_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    svmNonLinear_hog = test(SVM_nonLinear, 'hog', hog, 1, 15, (5,5), (1,1))
    print(" |->HOG orientations=15, pixels_per_cell=(5, 5), cells_per_block=(1, 1):", svmNonLinear_hog)
    deleteTrain("hog")
    deleteFullTrain("hog")
    svmNonLinear_hog = test(SVM_nonLinear, 'hog', hog, 1, 15, (5,5), (2,2))
    print(" |->HOG orientations=15, pixels_per_cell=(5, 5), cells_per_block=(2, 2):", svmNonLinear_hog)


if __name__ == '__main__':
    beginTests()