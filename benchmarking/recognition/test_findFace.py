from settings import PATH_IMAGES
import unittest
from findFace import findFace
import cv2 as cv

class TestFindFace(unittest.TestCase):
    def test_trueFace(self):
        #image = cv.imread('static/image/lena.jpg', cv.IMREAD_GRAYSCALE)
        image = cv.imread(PATH_IMAGES+'/s01/01.jpg', cv.IMREAD_GRAYSCALE)
        self.assertIsNotNone(image, 'Imagem não encontrada.')
    
        face, error = findFace(image)
        self.assertIsNone(error, error)

        self.assertGreater(len(face), 1, 'Face não encontrada')
    
    def test_falseFace(self):
        image = cv.imread(PATH_IMAGES+'/s01/01.jpg', cv.IMREAD_GRAYSCALE)
        self.assertIsNotNone(image, 'Imagem não encontrada.')
    
        face, error = findFace(image)
        self.assertIsNone(error, error)

        #teste para imagens sem faces
        #self.assertLess(len(face), 1, 'Face encontrada')


if __name__ == "__main__":
    unittest.main()