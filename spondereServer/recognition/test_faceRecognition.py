import os
from recognition.featureExtraction import train
from settings import EIGENFACES_NUMBER_COMPONENTS, PATH_IMAGES
from util.image import loadUserDataset
from recognition.faceRecognition import faceRecognition, verifyFace

def accuracy(path:str) -> float:
    fullPath = './'+path+'/'
    directories = os.listdir(fullPath)
    total: int = 0
    hit: int = 0

    for directory in directories:
        if os.path.isdir(fullPath +directory):
            subTotal, SubHit = testUserBiometrics(fullPath, directory)
            total = total + subTotal
            hit = hit + SubHit
    
    if total != 0:
        return hit/total
    return 0

def testUserBiometrics(path, userID):
    total: int = 0
    hit: int = 0
    pathTestFalse = '/false'
    pathTestTrue = '/true'
    label = 'tem que carregar os abels'

    featuresTrain, error = train(path, userID, EIGENFACES_NUMBER_COMPONENTS)
    if error != None:
        raise Exception(error)

    images = loadUserDataset(path+'/'+userID, pathTestFalse)
    total = total + len(images)

    for image in images:
        result, error = faceRecognition(image)
        if error == None:
            if not result:
                hit = hit + 1
        else: total = total - 1
   

    images = loadUserDataset(path + '/'+ userID, pathTestTrue)
    total = total + len(images)

    for image in images:
        result, error = verifyFace(featuresTrain, label, image, EIGENFACES_NUMBER_COMPONENTS)
        if error == None:
            if result:
                hit = hit + 1
        else: total = total - 1

    print(str(total)+" : "+ str(hit))
    
    return total, hit

if __name__ == '__main__':
    print(accuracy(PATH_IMAGES))
