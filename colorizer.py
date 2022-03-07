import numpy as np
import cv2
import logging
import os.path

class Colorizer:

    __prototxt = 'model/colorization_deploy_v2.prototxt'
    __model = 'model/colorization_release_v2.caffemodel'
    __points = 'model/center_pts.npy'

    def __init__(self):
        self.__points = os.path.join(os.path.dirname(__file__), self.__points)
        self.__prototxt = os.path.join(os.path.dirname(__file__), self.__prototxt)
        self.__model = os.path.join(os.path.dirname(__file__), self.__model)

        if not os.path.isfile(self.__model):
            logging.critical("A critical error occurred whilst initializing the data model file.")
            exit()

        self.__net = cv2.dnn.readNetFromCaffe(self.__prototxt, self.__model)
        self.__pts = np.load(self.__points)

        class8 = self.__net.getLayerId("class8_ab")
        conv8 = self.__net.getLayerId("conv8_313_rh")
        self.__pts = self.__pts.transpose().reshape(2, 313, 1, 1)
        self.__net.getLayer(class8).blobs = [self.__pts.astype("float32")]
        self.__net.getLayer(conv8).blobs = [np.full([1, 313], 2.606, dtype="float32")]

    def colorize_image(self, image_filename=None, cv2_frame=None):
        # load the input image from disk, scale the pixel intensities to the range [0, 1], and then convert the image from the BGR to Lab color space
        image = cv2.imread(image_filename) if image_filename else cv2_frame
        scaled = image.astype("float32") / 255.0
        lab = cv2.cvtColor(scaled, cv2.COLOR_RGB2Lab)

        # resize the Lab image to 224x224 (the dimensions the colorization network accepts), split channels, extract the 'L' channel, and then perform mean centering
        resized = cv2.resize(lab, (224, 224))
        L = cv2.split(resized)[0]
        L -= 50

        # pass the L channel through the network which will *predict* the 'a' and 'b' channel values
        self.__net.setInput(cv2.dnn.blobFromImage(L))
        ab = self.__net.forward()[0, :, :, :].transpose((1, 2, 0))

        # resize the predicted 'ab' volume to the same dimensions as our input image
        ab = cv2.resize(ab, (image.shape[1], image.shape[0]))

        # grab the 'L' channel from the *original* input image (not the resized one) and concatenate the original 'L' channel with the predicted 'ab' channels
        L = cv2.split(lab)[0]
        colorized = np.concatenate((L[:, :, np.newaxis], ab), axis=2)

        # convert the output image from the Lab color space to RGB, then clip any values that fall outside the range [0, 1]
        colorized = cv2.cvtColor(colorized, cv2.COLOR_LAB2RGB)
        colorized = np.clip(colorized, 0, 1)

        # the current colorized image is represented as a floating point data type in the range [0, 1] -- let's convert to an unsigned 8-bit integer representation in the range [0, 255]
        colorized = (255 * colorized).astype("uint8")
        return image, colorized
