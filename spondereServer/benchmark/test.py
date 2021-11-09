from settings import(
    PATH_IMAGES
)
import os

from util.image import loadImages


def test(classifier, extractMethod) -> float:
    count:int = 0
    hits:int = 0 

    directories = os.listdir(PATH_IMAGES)

    for directorie in directories:
        if os.path.isdir(os.path.join(PATH_IMAGES, directorie)):
            if (os.path.exists(os.path.join(PATH_IMAGES, directorie, 'false')) and 
                os.path.exists(os.path.join(PATH_IMAGES, directorie, 'true'))):
                
                tempCount, tempHits = testImages(directorie, classifier, extractMethod, 'false')
                count = count + tempCount
                hits = hits + tempHits

                tempCount, tempHits = testImages(directorie, classifier, extractMethod, 'true')
                count += tempCount
                hits += tempHits
    
    if count == 0: return 0

    return (hits/count)

def testImages(userID, classifier, extractMethod, folder):
    path = os.path.join(PATH_IMAGES, userID, folder)
    images = loadImages(path)

    hits = 0
    count = 0
    for image in images:
        if classifier(image, userID, extractMethod): hits += 1
        count += 1
    
    return count, hits


if __name__ == '__main__':

    euclidianDistance_eigen = test()
    euclidianDistance_lbp = test()
    euclidianDistance_hog = test()

    knn_lbp = test()
    knn_eigen = test()
    knn_hog = test()

    svm_lbp = test()
    svm_eigen = test()
    svm_hog = test()

    print("Distancia euclidiana:")
    print(" |->Eigenfaces: ", euclidianDistance_eigen)
    print(" |->LBP: ", euclidianDistance_lbp)
    print(" |->HOG: ", euclidianDistance_hog)

    print("KNN:")
    print(" |->Eigenfaces: ", knn_eigen)
    print(" |->LBP: ", knn_lbp)
    print(" |->HOG: ", knn_hog)

    print("SVM(linear):")
    print(" |->Eigenfaces: ", svm_eigen)
    print(" |->LBP: ", svm_lbp)
    print(" |->HOG: ", svm_hog)

