from skimage.feature import hog
import numpy as np

#hog features
def extractFeature(images):
    features = []
    for image in images:
        hogImage = hog(image, orientations=15, pixels_per_cell=(5, 5), cells_per_block=(1, 1))
        features.append(hogImage)

    return np.array(features, dtype=float)