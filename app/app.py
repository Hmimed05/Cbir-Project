import os
from io import BytesIO
from PIL import Image
from collections import Counter
import cv2


from Descriptors.color.colordescriptor import ColorDescriptor
from Descriptors.shape.fourierdescriptor import FourierDescriptor
from Descriptors.coocurence.concrunacescript import Concurence

import numpy as np
import shutil
import time
from flask import *

app = Flask(__name__)
FEATURES_COLOR_PATH = 'app/database/color.csv'
FEATURES_TEXTURE_PATH = 'app/database/concurence.csv'
FEATURES_FOURIER_PATH = 'app/database/fourier.csv'



distances = {}


def showSimilarity(filename):
    files = {}
    index = 0
    global distances
    try:
        color_distance, texture_distance, fourier_distance = getDistanceOfAllPictures(
            filename)
        distances['filename'] = filename
        distances['data'] = [color_distance,texture_distance, fourier_distance]
        results = distanceTotal(
            color_distance, texture_distance, fourier_distance)
        results = sorted([(v, k) for (k, v) in results.items()])

        print("End Calc Similarity We Just Return 10 Pictures")
        for f in results[:50]:
            files[index] = f[1]
            index = index + 1
    except Exception as identifier:
        print(identifier)
        status_num = 0
        distances = {}

    return files


def changeWeights(filename):
    index = 0
    files = {}
    if (distances.get('filename') == filename):
        results = distanceTotal(
            distances['data'][0], distances['data'][1], distances['data'][2], retour=True)
        results = sorted([(v, k) for (k, v) in results.items()])
        print("End Calc Similarity We Just Return 50 Pictures")
        for f in results[:50]:
            files[index] = f[1]
            index = index + 1

    return {'status': 1, 'message': files}


def getDistanceOfAllPictures(filename):
    # initialize the color descriptor
    colorDesc = ColorDescriptor((8, 12, 3), FEATURES_COLOR_PATH)
    textDesc = Concurence(FEATURES_TEXTURE_PATH)
    fourierDesc = FourierDescriptor(FEATURES_FOURIER_PATH)
    imagePath = filename
    #print(filename)
    image = cv2.imread(imagePath)
    # descriptor Of Color
    features_color = colorDesc.describe(image)
    # Descriptor Of Texture
    features_texture = textDesc.getTextureDescOfPic(image)
    # Descriptor Of Fourier
    features_fourier = fourierDesc.calcFourierDescriptor(image)
    print("Start Calc Similarity Of Our Picture")
    return colorDesc.search(features_color), textDesc.calcDistance(features_texture), fourierDesc.calcDistance(features_fourier)
# close the index file


def distanceTotal(color_distance, texture_distance, fourier_distance, retour=False):
    print("innnnnnnnn")
    # Define Weights
    if (retour):
        color_weight, texture_weight, fourier_weight = getWeights()
    else:
        color_weight, texture_weight, fourier_weight = [1/3, 1/3, 1/3]
    for key in color_distance:
        color_distance[key] *= color_weight

    for key in texture_distance:
        texture_distance[key] *= texture_weight

    for key in fourier_distance:
        fourier_distance[key] *= fourier_weight
    # So Here Will Return For Each Picture Just Unique Value As  Distance Global
    distTotal = Counter(color_distance) + \
        Counter(texture_distance) + Counter(fourier_distance)
    #print(distTotal)
    return distTotal


def getWeights():
    while (True):
        weights = np.random.rand(3)
        if (np.sum(weights) < 1 and np.sum(weights) >= 0.99):
            break
    return weights




@app.route('/', methods=['GET', 'POST'])
def basic():
    #print(SimilarColorsImages("app\queries\gh.jpg"))
    return render_template('index.html')

# search route
@app.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        isthisFile=request.files.get('file')
        #print(isthisFile)
        #print(isthisFile.filename)
        isthisFile.save("app/queries/"+isthisFile.filename)
        # get url
        image_url = 'app/queries/'+ isthisFile.filename
        #print(image_url)
        try:
            results = showSimilarity(image_url)
            #print(changeWeights(image_url))
            #print(results)
            #jsonify(results)
            return results
        except:
            # return error
            jsonify({"sorry": "Sorry, no results! Please try again."}), 500



if __name__ == '__main__':
	app.run(debug=True)
