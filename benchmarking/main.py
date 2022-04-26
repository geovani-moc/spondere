from util.recognition import deleteFullTrain, deleteTrain
from benchmark.test import beginTests
from benchmark.testCNN import CNNTests

if __name__ == '__main__':
    '''
    deleteTrain("eigen")
    deleteTrain("lbp")
    deleteTrain("hog")
    deleteTrain("cnn")

    deleteFullTrain("eigen")
    deleteFullTrain("lbp")
    deleteFullTrain("hog")
    deleteFullTrain("cnn")
    #'''
    #beginTests()
    CNNTests()