from threading import Thread
import cv2
import vision

class BasketGet:
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
            #self.info = vision.apply_ball_color_filter(hsv,True)
            #print(self.info[0:2])
            #cv2.imshow("korv",self.info[3])
            #cv2.imshow("test", self.frame)

            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True