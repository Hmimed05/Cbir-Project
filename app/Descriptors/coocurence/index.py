# import the necessary packages
from concrunacescript import Concurence
import argparse
import glob
import cv2 as cv


# initialize the color descriptor
ConcurenceModule = Concurence()

# open the output index file for writing
output = open("app/database/concurence.csv", "w")
# use glob to grab the image paths and loop over them
for imagePath in glob.glob("app/static/dataset/**/*.*",recursive = True):
    # extract the image ID (i.e. the unique filename) from the image
    # path and load the image itself
    imageID = imagePath[imagePath.rfind("/") + 1:]
    image = cv.imread(imagePath)
    # describe the image
    features = ConcurenceModule.getTextureDescOfPic(image)
    # write the features to file
    features = [str(f) for f in features]
    output.write("%s,%s\n" % (imageID, ",".join(features)))
# close the index file
output.close()
