from util.recognition import deleteFullTrain, deleteTrain, deleteFullTrain

if __name__ == '__main__':
    deleteTrain("eigen")
    deleteTrain("lbp")
    deleteTrain("hog")

    deleteFullTrain("eigen")
    deleteFullTrain("lbp")
    deleteFullTrain("hog")