import face_recognition
import numpy as np
from util.recognition import loadFullLabels, loadFullTrain
import os
import glob

def verifyFace(image, userID, name, featureMethod, args):
    featuresTest = face_recognition.face_encodings(image)[0]
    features, _ = loadFullTrain(name, featureMethod, args)
    labels = loadFullLabels(name)

    if len(labels) != len(features): return False, "caracteristicas e rotulos não coincidem"
    if len(features) == 0: return False, None

    ##classificador
    result = face_recognition.compare_faces(features, featuresTest)
     
    label = ""
    if True in result:
        firstMatchIndex = result.index(True)
        label = labels[firstMatchIndex]

    if  label == userID: return True, None

    return False, None


def train(path:str):
    features = []
    labels = []
    directories = os.listdir(path)

    for directorie in directories:
        filePath = os.path.join(path, directorie)
        files = os.listdir(filePath)
        for file in files:
            if os.path.isfile(os.path.join(filePath, file)):
                image = face_recognition.load_image_file(os.path.join(filePath, file))
                feature = face_recognition.face_encodings(image)[0]
                features.append(feature)
                labels.append(directorie)

    if len(labels)!= len(features):
        raise Exception("Quantidae de caracteristicas e rotulos divergem.")

    return features, labels