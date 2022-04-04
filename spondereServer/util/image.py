from pathlib import Path
import cv2 as cv
import glob
import sys
import numpy as np
from io import BytesIO
import zipfile
import json
from settings import noImage
import zlib

def saveBinaryImagesInDataset(images, pathDataset:str, userCode:int):
    count:int = 1
    if(len(images) < 1): return 'Erro nenhuma foi enviada para o dataset.' 
    Path(pathDataset+ '/'+ str(userCode) +'/' ).mkdir(parents=True, exist_ok=True)

    for image in images:
        path = pathDataset+ '/'+ str(userCode) +'/' + str(count) + '.jpg'
        # with open(path, "wb") as buffer:
        #     shutil.copyfileobj(image, buffer)
        cv.imwrite(path, image)
        count = count+1

    return None

def imageResized(image, height, width):
    dim = (width, height)
    result = cv.resize(image, (dim), interpolation=cv.INTER_AREA)
    return result

def checkUploadedImage(file):
    try:
        decode_img = cv.imdecode(np.frombuffer(file, np.uint8), -1)
    except:
        return None
    else:
        return decode_img

def loadImages(path:str):
    images = []
    pathImages = glob.glob(path+'/*.jpg')

    for pathImage in pathImages: 
        image = cv.imread(pathImage, cv.IMREAD_GRAYSCALE)
        if image is None:
            print("Nenhuma imagem carregada do dataset.")
        else:
            images.append(image)

    return images

def loadUserDataset(path:str, userID:int):
    images = []

    types = ('/*.jpg', '/*.jpeg')
    pathImages = []
    for imagesType in types:
        pathImages.extend(glob.glob(path+"/"+str(userID)+imagesType))

    for pathImage in pathImages: 
        image = cv.imread(pathImage, cv.IMREAD_GRAYSCALE)
        image = cv.equalizeHist(image)
    
        if image is None:
            print("Erro loaddataset, erro ao carregar imagem.", file=sys.stderr)
        else:
            images.append(image)

    return images

def printFeature(pcaImage, imageSize, name = 'Teste'):
    image = pcaImage.reshape(imageSize, imageSize)
    norm_image = cv.normalize(image, None, alpha = 0, beta = 255, norm_type = cv.NORM_MINMAX, dtype = cv.CV_32F)
    norm_image = norm_image.astype(np.uint8)
    cv.imshow(name, norm_image)
    cv.waitKey()
    cv.destroyWindow(name)

def zipPresentStudentsImages(texts, images):
    isSuccess, bufferNoImage = cv.imencode(".jpg", noImage)
    if not isSuccess:
        print("Imagem default não foi carregada.")

    buffer = []
    jsonTexts = json.dumps(texts).encode()
    buffer.append(("names.json", jsonTexts))

    for index, image in enumerate(images):
        path:str = texts[index] + ".jpg"
        if image is not None:
            isSuccess, bufferImage = cv.imencode(".jpg", image)
            buffer.append((path, bufferImage))
        else:
            buffer.append((path, bufferNoImage))

    return generateZip(buffer)

def generateZip(files):
    memoryZip = BytesIO()

    with zipfile.ZipFile(memoryZip, mode="w", compression=zipfile.ZIP_DEFLATED) as zippedFiles:
        for file in files:
            zippedFiles.writestr(file[0], file[1])

    return memoryZip.getvalue()
