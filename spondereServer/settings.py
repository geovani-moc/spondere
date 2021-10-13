import cv2 as cv

FACE_DIM = 50
PATH_IMAGES = 'recognition/dataset'
PATH_DATA_TRAIN = 'static/train'
EIGENFACES_NUMBER_COMPONENTS = 50
MIN_SIZE_DATASET = 5
THRESHOLD = 2200

faceCascade = cv.CascadeClassifier('static/xml/haarcascade_frontalface_default.xml')
eyeCascade = cv.CascadeClassifier('static/xml/haarcascade_eye.xml')
PATH_CLASSIFIER_TRAIN ='static/xml/face_classifier.xml'

USER_TYPE_PROFESSOR = 1
USER_TYPE_STUDENT = 2
USER_TYPE_ADMIN = 3

USER_ACCOUNT_ACTIVATED = 1
USER_ACCOUNT_DESACTIVATED = 2

EIGENFACES = 1
HOG = 2
LBP = 3
EUCLEDIAN_DISTANCE = 1
KNN = 2
SVM = 3
