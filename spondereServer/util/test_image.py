import unittest
from util.image import saveBinaryImagesInDataset, loadUserDataset
from settings import PATH_IMAGES, MIN_SIZE_DATASET
import cv2 as cv
import numpy as np


class TestUtil(unittest.TestCase):
    def test_SaveBinaryImagesInDataset(self):
        image = cv.imread(PATH_IMAGES+"/s01/01.jpg")
        image = np.asarray(image)
        images = [image]
        error = saveBinaryImagesInDataset(images, PATH_IMAGES, '01_test')
        self.assertIsNone(error, error)

    def testLoad(self):
        path = PATH_IMAGES
        userID = 's01'
        images = loadUserDataset(path, userID)
        self.assertGreater(len(images), MIN_SIZE_DATASET, "Erro ao carregar dataset, não foi carregado a quantidade adequada de imagens.")


if __name__ == '__main__':
    unittest.main()