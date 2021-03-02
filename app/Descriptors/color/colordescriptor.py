import numpy as np
import cv2
import imutils
import csv


class ColorDescriptor:
	def __init__(self, bins, indexPath=None):
		self.bins = bins
		self.indexPath = indexPath

	def describe(self, image):
		image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
		features = []

		(h, w) = image.shape[:2]
		(cX, cY) = (int(w * 0.5), int(h * 0.5))

		segments = [(0, cX, 0, cY), (cX, w, 0, cY), (cX, w, cY, h),
			(0, cX, cY, h)]

		(axesX, axesY) = (int(w * 0.75) // 2, int(h * 0.75) // 2)
		ellipMask = np.zeros(image.shape[:2], dtype = "uint8")
		cv2.ellipse(ellipMask, (cX, cY), (axesX, axesY), 0, 0, 360, 255, -1)

		for (startX, endX, startY, endY) in segments:
			cornerMask = np.zeros(image.shape[:2], dtype = "uint8")
			cv2.rectangle(cornerMask, (startX, startY), (endX, endY), 255, -1)
			cornerMask = cv2.subtract(cornerMask, ellipMask)

			hist = self.histogram(image, cornerMask)
			features.extend(hist)

		hist = self.histogram(image, ellipMask)
		features.extend(hist)
		#print(features)
		return features

	def histogram(self, image, mask):
		hist = cv2.calcHist([image], [0, 1, 2], mask, self.bins,
			[0, 180, 0, 256, 0, 256])

		if imutils.is_cv2():
			hist = cv2.normalize(hist).flatten()

		else:
			hist = cv2.normalize(hist, hist).flatten()

		return hist
	def search(self, queryFeatures):
		# initialize our dictionary of results
		results = {}

        # open the index file for reading
		with open(self.indexPath) as f:
			# initialize the CSV reader
			reader = csv.reader(f)
			# loop over the rows in the index
			for row in reader:
				# parse out the image ID and features, then compute the
				# chi-squared distance between the features in our index
				# and our query features
				features = [float(x) for x in row[1:]]
				d = self.chi2_distance(features, queryFeatures)
				# now that we have the distance between the two feature
				# vectors, we can udpate the results dictionary -- the
				# key is the current image ID in the index and the
				# value is the distance we just computed, representing
				# how 'similar' the image in the index is to our query
				results[row[0]] = d
			# close the reader
			f.close()
		# sort our results, so that the smaller distances (i.e. the
		# more relevant images are at the front of the list)
		#print(results)
		return results

	def chi2_distance(self, histA, histB, eps = 1e-10):
		# compute the chi-squared distance
		d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
			for (a, b) in zip(histA, histB)])
		# return the chi-squared distance
		return d