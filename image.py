import os.path

import cv2


class ImageColorizer:

    def __init__(self, imageName):
        self.imageName = imageName
        self.baseImageName = os.path.splitext(self.imageName)[0]
        self.imagePath = os.path.join(os.path.dirname(__file__), 'images', self.imageName)

    def colorize(self, colorizer):

        (original, colorized) = colorizer.colorize_image(self.imagePath)
        colored_frame_path = os.path.join(os.path.dirname(__file__), 'images', self.baseImageName + "-colored.jpg")

        cv2.imwrite(colored_frame_path, colorized)

        cv2.imshow("Original", original)
        cv2.imshow("Colorized", colorized)
        cv2.waitKey(0)
