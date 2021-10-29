from recognition.findFace import findFace
import cv2 as cv


def verifyFace(features, labels, image, label):
    image = cv.equalizeHist(image)
    face, error = findFace(image)
    if error is not None:
        return None, "error em localizar a face"

    images = []
    images.append(face)

    result = True
    return result, None


def faceRecognition(label, image):
    features, labels = loadFeatures()
    if len(features) < 1:
        return None, "Problemas com a base de treinamento, não foi possivel carregar."

    if len(image.shape) > 2:
        image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
    
    result, error = verifyFace(features, labels, image, label)

    if error is not None:
        return None, error

    return result, None

def loadFeatures():
    return ["features"], ["labels"]
    
if __name__ == '__main__':
    print("no tests")