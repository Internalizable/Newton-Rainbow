#!/usr/bin/env python

import sys

import colorizer
import video
import image


def main(args):
    colorizerInstance = colorizer.Colorizer()

    #videoInstance = video.VideoColorizer("football.mp4")

    #if videoInstance.loadVideo():
        #videoInstance.translate(colorizerInstance)

    imageInstance = image.ImageColorizer("paris-bw-colored.jpg")
    imageInstance.colorize(colorizerInstance)

if __name__ == '__main__':
    main(sys.argv)
