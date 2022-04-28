from settings import PATH_IMAGES
import unittest
from findFace import findFace
import cv2 as cv
import numpy as np

class TestFindFace(unittest.TestCase):
    def test_trueFace(self):
        image = cv.imread(PATH_IMAGES+'/s01/01.jpg')
        image = np.asarray(image)
        self.assertIsNotNone(image, 'Imagem não encontrada.')
    
        face, error = findFace(image)
        self.assertIsNone(error, error)

        self.assertGreater(len(face), 1, 'Face não encontrada')
    
    def test_falseFace(self):
        image = cv.imread(PATH_IMAGES+'/s01/01.jpg')
        image = np.asarray(image)
        self.assertIsNotNone(image, 'Imagem não encontrada.')
    
        face, error = findFace(image)
        self.assertIsNone(error, error)



if __name__ == "__main__":
    unittest.main()