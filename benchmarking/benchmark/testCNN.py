import face_recognition
import os
import glob
from cnn import train

def test(features, labels, path)->float:
    count:float = 0
    hits:float = 0 
    directories = os.listdir(path)

    for directorie in directories:
        if os.path.isdir(os.path.join(path, directorie)):
            if (os.path.exists(os.path.join(path, directorie, 'false')) and 
                os.path.exists(os.path.join(path, directorie, 'true'))):
                
                tempCount, tempHits = testImages(os.path.join(path, directorie, 'false'), directorie, features, labels)
                count = count + tempCount
                hits = hits + (tempCount - tempHits)

                tempCount, tempHits = testImages(os.path.join(path, directorie, 'true'), directorie, features, labels)
                count += tempCount
                hits += tempHits

    if count == 0: return 0.0

    print(f'acertos:{hits}\nQuantidade:{count}')

    return (hits/count)

def testImages(path, userID, features, labels):
    directories = os.listdir(path)
    hits:float = 0

    for directory in directories:
        image = face_recognition.load_image_file(os.path.join(path, directory))
        featureTest = face_recognition.face_encodings(image)[0]
        matches = face_recognition.compare_faces(features, featureTest)
        name = ""
        if True in matches:
            firstMatchIndex = matches.index(True)
            name = labels[firstMatchIndex]

            if name == userID: hits += 1
        
    count:float =  float(len(glob.glob1(path,"*.jp*")))
    return count, hits

if __name__ == '__main__':
    path = 'dataset'
    features, labels = train(path)
    acurracy = test(features, labels, path)

    print(f'Precisão: {acurracy*100}%')