from skimage.feature import local_binary_pattern
from skimage.feature import hog
from skimage.transform import resize
from skimage.io import imread
from skimage.color import rgb2gray

def extractFeatureLBP(image):
    lbp = local_binary_pattern(image, 8,1.0,method='default')
    return lbp


def extractFeatureEigenFaces(image):

    pass

def extractFeatureHOG(image):
    hog_image = hog(image, orientations=9, pixels_per_cell=(10, 10), cells_per_block=(1, 1))
    return hog_image

if __name__ == "__main__":
    image = imread('./static/image/eu.jpg')
    image = resize(image, (50, 50))
    image = rgb2gray(image)
    extractFeatureHOG(image)