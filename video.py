import os.path

import cv2


class VideoColorizer:

    fps = None

    def __init__(self, videoName):
        self.videoName = videoName
        self.baseVideoName = os.path.splitext(self.videoName)[0]
        self.baseVideoPath = os.path.join(os.path.dirname(__file__), 'videos', self.baseVideoName)

    def loadVideo(self):

        videoPath = os.path.join(os.path.dirname(__file__), 'videos', self.videoName)
        vidcap = cv2.VideoCapture(videoPath)

        try:
            os.mkdir(self.baseVideoPath)
        except FileExistsError as error:
            self.fps = vidcap.get(cv2.CAP_PROP_FPS)
            print("FPS found to be at ", self.fps)
            return True

        success, image = vidcap.read()
        count = 0

        while success:
            framePath = os.path.join(self.baseVideoPath, 'frame%d.jpg' % count)
            print(framePath)

            cv2.imwrite(framePath, image)  # save frame as JPEG file

            success, image = vidcap.read()
            print('Read a new frame: ', success)
            count += 1

    def translate(self, colorizer):
        frame_array = []
        files = [f for f in os.listdir(self.baseVideoPath) if os.path.isfile(os.path.join(self.baseVideoPath, f))]

        files.sort(key=lambda x: int(x[5:-4]))

        base_color_path = os.path.join(os.path.dirname(__file__), 'videos', self.baseVideoName + "-colored")

        try:
            os.mkdir(base_color_path)
        except FileExistsError as error:
            print("Directory already exists, passing to process pipeline")

        for i in range(len(files)):
            print("Processing frame ", i)

            colorized = None

            colored_frame_path = os.path.join(base_color_path, "frame" + str(i) + ".jpg")

            if os.path.exists(colored_frame_path):
                print("Colored frame already exists, appending...")
                colorized = cv2.imread(colored_frame_path)
            else:
                framePath = os.path.join(self.baseVideoPath, files[i])
                (original, colorized) = colorizer.colorize_image(framePath)

            height, width, layers = colorized.shape
            size = (width, height)

            frame_array.append(colorized)
            cv2.imwrite(colored_frame_path, colorized)

            print("Processed and appended to list")

        print("Finished processing all frames, creating video")

        outputPath = os.path.join(os.path.dirname(__file__), 'videos', self.baseVideoName + '-colored.mp4')

        out = cv2.VideoWriter(outputPath, cv2.VideoWriter_fourcc(*'DIVX'), self.fps, size)

        for i in range(len(frame_array)):
            out.write(frame_array[i])

        print("Written")
        out.release()
