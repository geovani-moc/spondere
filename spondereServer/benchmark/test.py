def test():
    return 0.0

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

