from threading import Thread
import cv2
import json
import numpy as np
import vision

kernel1 = np.ones((4,4), np.uint8)
try:
    with open("colors.json", "r") as f:
        saved_colors = json.loads(f.read())
except FileNotFoundError:
    saved_colors = {}
color = "green"
state = 0

if color in saved_colors:
    filters = saved_colors[color]
else:
    filters = {
        "min": [0, 0, 0], # HSV minimum values
        "max": [255, 255, 255] # HSV maximum values
    }
green = saved_colors["green"]

class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False
        self.info = None

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            bgr = self.frame
            hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
            self.info = vision.apply_ball_color_filter(hsv)
            #print(self.info[0:2])
            cv2.imshow("pilt",self.frame)
            cv2.imshow("dilaator",self.info[3])

            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True