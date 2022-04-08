from pathlib import Path
import cv2 as cv
import glob
import sys
import numpy as np
from io import BytesIO
import zipfile
import json
import zlib
import base64

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

def encodePresentStudentsImages(texts, images):

    if len(texts) != len(images): 
        raise ValueError("Erro, quantidade de nomes diferente de imagens.")

    buffer = []

    for index, image in enumerate(images):
        if image is not None:
            _, bufferImage = cv.imencode(".jpg", image)
            imageBase64 = (base64.b64encode(bufferImage)).decode("utf-8")

            buffer.append({
                "name":texts[index],
                "biometry":True,
                "encode":"jpg/base64",
                "image": imageBase64
            })
        else:
            buffer.append({
                "name":texts[index],
                "biometry":False,
                "encode": None,
                "image": None
            })

    #presents = json.dumps({"presents":buffer})
    presents = {"presents":buffer}
    return presents

def generateZip(files):
    memoryZip = BytesIO()

    with zipfile.ZipFile(memoryZip, mode="w", compression=zipfile.ZIP_DEFLATED) as zippedFiles:
        for file in files:
            zippedFiles.writestr(file[0], file[1])

    return memoryZip.getvalue()
