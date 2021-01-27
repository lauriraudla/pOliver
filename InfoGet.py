from threading import Thread
import cv2
import vision

class BallGet:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, frame=None, basket=False):
        self.frame = frame
        self.stopped = False
        self.info = None
        self.info2 = None
        self.info3 = None
        self.basket = basket
        self.ready = False

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            self.ready = False
            bgr = self.frame
            #bgr = bgr[0:660,0:1279]
            hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
            #cv2.imshow("hsv", hsv)
            #hsv = self.frame
            #korv
            self.info2 = vision.apply_ball_color_filter(hsv, True)
            #piir
            self.info3 = vision.apply_ball_color_filter(hsv, False, True, None)
            #pall
            self.info = vision.apply_ball_color_filter(hsv, False, False, self.info2[5], self.info3[3])
            #if self.basket:
            #    self.info = vision.apply_ball_color_filter(hsv,True)
            #print(self.info[0:2])
            cv2.imshow("pall",self.info[3])
            #cv2.resizeWindow('pall', 640, 480)
            cv2.imshow("korv",self.info2[3])
            #cv2.resizeWindow('korv', 640, 480)
            #cv2.imshow("edge", self.info3[3])
            #cv2.resizeWindow('edge', 640, 480)

            if cv2.waitKey(1) == ord("q"):
                self.stop()

    def stop(self):
        self.stopped = True