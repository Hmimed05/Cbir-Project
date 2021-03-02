import cv2 as cv
import numpy as np
import csv
from scipy.spatial.distance import euclidean


class FourierDescriptor():

    def __init__(self, indexPath=None):
        # Path Of our index : Descriptor
        self.indexPath = indexPath

    def findContours(self):
        # Grayscale transformation and binarization
        grayImage = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        # Find Canny edges
        edged = cv.Canny(grayImage, 50, 200)
        #  Find outer contour*
        contours, hireachy = cv.findContours(
            edged, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
        self.contours = contours

    # Calculate the Fourier descriptor of the contour
    def calcFourierDescriptor(self, img):
        self.img = img
        # Find Contours
        self.findContours()
        s = len(self.contours)
        f = []  # The actual descriptor of the contour
        for u in range(s):
            sumx = 0
            sumy = 0
            for j in range(len(self.contours[u])):
                p = self.contours[u][j][0]
                if (len(p) < 2):
                    continue
                x = p[0]
                y = p[1]
                sumx += (float)(x*np.cos(2*np.pi*u*j/s) +
                                y*np.sin(2 * np.pi*u*j / s))
                sumy += (float)(y*np.cos(2 * np.pi*u*j / s) -
                                x*np.sin(2 * np.pi*u*j / s))
            f.append(np.sqrt((sumx * sumx) + (sumy * sumy)))

        return self.normlizeFeatures(f)

    # Normalization of Fourier description characters
    def normlizeFeatures(self, desc):
        fd = []  # Descriptor after normalization, and take the first 15 Value
        desc[0] = 0
        fd.append(0)
        if (len(desc) < 17):
            for n in range(17-len(desc)):
                desc.append(0)
        for k in range(2, 17):
            if (desc[1] == 0):
                out = 0
            else:
                out = desc[k] / desc[1]
            fd.append(out)
        return fd

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
        #print(results)
        return results

    def normalizeOurDistance(self, feature, qfeature):
        return euclidean(feature, qfeature)
