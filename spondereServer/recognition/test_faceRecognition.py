import os
import cv2 as cv
from recognition.faceRecognition import  verifyFace
from settings import PATH_IMAGES
from recognition.findFace import findFace

def test_recognition(image, user):
    result, _ = verifyFace(image=image, userID=user)
    return result

if __name__ == '__main__':
    image1 = cv.imread(os.path.join(PATH_IMAGES, 's01', '01.jpg'), cv.IMREAD_GRAYSCALE)
    face, error = findFace(image1)
    if error is None:
        result = test_recognition(face, 's01')
        print("result:",  result)

        result = test_recognition(face, 's04')
        print("result:",  result)
    else: print("False")
