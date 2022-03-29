from settings import PATH_IMAGES, MIN_SIZE_DATASET, EIGENFACES_NUMBER_COMPONENTS
from recognition.featureExtraction import train
from recognition.faceRecognition import createDataFeatures, verifyFace
import unittest
from util.image import loadUserDataset

class test_recognition(unittest.TestCase):
    
    def testTrueFaceRecognition(self):
        path = PATH_IMAGES
        userID = 's01'
        pathTestTrue = 's01/true'

        featuresTrain, error = train(path, userID, EIGENFACES_NUMBER_COMPONENTS)
        self.assertIsNone(error, error)
        
        images = loadUserDataset(path, pathTestTrue)
        for image in images:
            threshold, error = verifyFace(featuresTrain, image, EIGENFACES_NUMBER_COMPONENTS)
            self.assertIsNone(error, error)
            # self.assertLess(threshold, THRESHOLD)
            print(f'limiar = {threshold}')

    def testFalseFaceRecognition(self):
        path = PATH_IMAGES
        userID = 's01'
        pathTestFalse = 's01/false'

        featuresTrain, error = train(path, userID, EIGENFACES_NUMBER_COMPONENTS)
        self.assertIsNone(error, error)
        
        images = loadUserDataset(path, pathTestFalse)
        for image in images:
            threshold, error = verifyFace(featuresTrain, image, EIGENFACES_NUMBER_COMPONENTS)
            self.assertIsNone(error, error)
            # self.assertGreater(threshold, THRESHOLD)
            print(f'limiar = {threshold}')
    
    def testCreateDataFeatures(self):
        error = createDataFeatures()
        self.assertIsNone(error, error)




if __name__ == '__main__':
    unittest.main()
