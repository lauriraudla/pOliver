from threading import Thread
import cv2

class VideoGet:
    """
    Class that continuously gets frames from a VideoCapture object
    with a dedicated thread.
    """

    def __init__(self, src=4):
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
        self.stream.set(cv2.CAP_PROP_EXPOSURE, 120.0)
        self.stream.set(cv2.CAP_PROP_AUTO_WB, 0)
        self.stream.set(cv2.CAP_PROP_WB_TEMPERATURE, 5700)
        self.stream.set(3, 1280)
        self.stream.set(4, 720)
        (self.grabbed, self.frame) = self.stream.read()
        self.stopped = False

    def start(self):
        Thread(target=self.get, args=()).start()
        return self

    def get(self):
        while not self.stopped:
            if not self.grabbed:
                self.stop()
            else:
                (self.grabbed, self.frame) = self.stream.read()

    def stop(self):
        self.stopped = True