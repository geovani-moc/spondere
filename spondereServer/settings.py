import cv2 as cv
import numpy as np

FACE_DIM = 50
PATH_IMAGES = 'recognition/dataset'
PATH_DATA_TRAIN = 'static/train'
EIGENFACES_NUMBER_COMPONENTS = 50
MIN_SIZE_DATASET = 6 #para teste =3, para uso = 6
NUMBER_FEATURES_DATASET = 10
THRESHOLD = 2200

VALIDATION_CODE_SIZE = 10

faceCascade = cv.CascadeClassifier('static/xml/haarcascade_frontalface_default.xml')
eyeCascade = cv.CascadeClassifier('static/xml/haarcascade_eye.xml')
PATH_CLASSIFIER_TRAIN ='static/xml/face_classifier.xml'

USER_TYPE_ADMIN = 1
USER_TYPE_PROFESSOR = 2
USER_TYPE_STUDENT = 3

USER_ACCOUNT_ACTIVATED = 1
USER_ACCOUNT_DESACTIVATED = 2

SVM_HOG = np.array([], float)
LABELS = np.array([], str)

TIMEZONE_API_SERVER = "-03:00"