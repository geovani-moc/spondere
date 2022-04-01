from util.recognition import deleteFullTrain, deleteTrain
from benchmark.test import beginTests

if __name__ == '__main__':
    deleteTrain("eigen")
    deleteTrain("lbp")
    deleteTrain("hog")

    deleteFullTrain("eigen")
    deleteFullTrain("lbp")
    deleteFullTrain("hog")

    beginTests()    