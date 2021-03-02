import cv2 as cv
import numpy as np
import mahotas as mhtos
from scipy.spatial.distance import euclidean
import csv


class Concurence():
    def __init__(self, indexPath=None):
        # store our index path
        self.indexPath = indexPath

    def getTextureDescOfPic(self, img):
        img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        features_texture = mhtos.features.haralick(img_gray).mean(axis=0)
        return features_texture

    # @params : queryFeature => image uploaded
    # @Params : feature => our Images That already Exist in our Application
    def calcDistance(self, queryFeature):
        # initialize our dictionary of results
        results = {}
        # open the index file for reading
        with open(self.indexPath) as f:
            # initialize the CSV reader
            reader = csv.reader(f)
            # loop over the rows in the index
            for row in reader:
                # parse out the image Name and features, then compute the
                # Euclidean distance between the features in our index
                # and our query features
                feature = [float(x) for x in row[1:]]
                d = self.normalizeOurDistance(feature, queryFeature)
                # now that we have the distance between the two feature
                # vectors, we can udpate the results dictionary -- the
                # key is the current image Name in the index and the
                # value is the distance we just computed, representing
                # how 'similar' the image in the index is to our query
                results[row[0]] = d
            # close the reader File
            f.close()
        # sort our results, so that the smaller distances (i.e. the
        # more relevant images are at the front of the list
        #print("concurence : "+results)
        return results

    def normalizeOurDistance(self, feature, qfeature):
        return euclidean(feature, qfeature)
