import cv2 as cv

FACE_DIM = 100
PATH_IMAGES = 'recognition/dataset'
PATH_DATA_TRAIN = 'static/train'
MIN_SIZE_DATASET = 1 
MAX_SIZE_DATASET = 5
NUMBER_FEATURES_DATASET = 5

VALIDATION_CODE_SIZE = 10

faceCascade = cv.CascadeClassifier('static/xml/haarcascade_frontalface_default.xml')
PATH_CLASSIFIER_TRAIN ='static/xml/face_classifier.xml'

USER_TYPE_ADMIN = 1
USER_TYPE_PROFESSOR = 2
USER_TYPE_STUDENT = 3

USER_ACCOUNT_ACTIVATED = 1
USER_ACCOUNT_DESACTIVATED = 2

TIMEZONE_API_SERVER = "-03:00"