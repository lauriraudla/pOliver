import pyrealsense2 as rs
import numpy as np
from threading import Thread
import cv2

#TODO: add a depth stream and a method for returning depth data
#also see https://github.com/ReikoR/bbr18-software/blob/001TRT/goal_distance/goal_distance.py
#for one way of reading depth data.

class imageCapRS2:
    def commandThread(self):
        while self.running:
            self.frames = self.pipeline.wait_for_frames()
            self.color_frame = self.frames.get_color_frame()
            self.currentFrame = np.asanyarray(self.color_frame.get_data())


    def __init__(self, src=0):
        #create initial variables for use in methods
        self.running = True
        self.depth_image = None
        self.currentFrame = None

        #create and start the pipeline with a color image stream
        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, 800, 600, rs.format.bgr8, 60)
        self.pipeline.start(self.config)
        #color = a.get_device().query_sensors()[1]
        #color.set_option(rs.option.enable_auto_exposure, 0)
        #color.set_option(rs.option.exposure, 120)
        #color.set_option(rs.option.enable_auto_white_balance, 0)
        #color.set_option(rs.option.white_balance, 5700)

        #initialize the values for the frame related variables
        self.frames = self.pipeline.wait_for_frames()
        self.color_frame = self.frames.get_color_frame()
        self.currentFrame = np.asanyarray(self.color_frame.get_data())
        Thread(name="commandThread", target=self.commandThread).start()


    def getFrame(self):
        return self.currentFrame

    def setStopped(self, stopped):
        self.pipeline.stop()
        self.running = stopped

    def findBall(self, cut, filters):
        kernel1 = np.ones((1, 1), np.uint8)
        blur = cv2.blur(cut, (3, 3))
        # 4. Use filters on HSV image
        mask = cv2.inRange(blur, tuple(filters["min"]), tuple(filters["max"]))
        bilateral = cv2.bilateralFilter(mask, 5, 175, 175)
        # 5. morphological actions
        opened = cv2.morphologyEx(bilateral, cv2.MORPH_OPEN, kernel1)
        # detect circles
        circles = cv2.HoughCircles(opened, cv2.HOUGH_GRADIENT, 1, minDist=100, param1=400, param2=1, minRadius=3,
                                   maxRadius=50)
        # draw circles
        if circles is not None:
            pt = np.round(circles[0, :]).astype("int")
            for (x, y, r) in pt:
                cv2.circle(cut, (x, y), r, (0, 255, 0), 4)

        return circles


