import cv2, threading

class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print("starting" + self.previewName)
        camPreview(self.previewName, self.camID)


def camPreview(previewName, camID):
    cv2.namedWindow(previewName)
    cam = cv2.VideoCapture(camID)
    cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    cam.set(cv2.CAP_PROP_EXPOSURE, 120.0)
    cam.set(cv2.CAP_PROP_AUTO_WB, 0)
    cam.set(cv2.CAP_PROP_WB_TEMPERATURE, 5700)
    if cam.isOpened():
        rval, frame = cam.read()
    else:
        rval = False

    while rval:
        return rval, frame
    # while rval:
    #     cv2.imshow(previewName, frame)
    #     rval, frame = cam.read()
    #     key = cv2.waitKey(10)
    #     if key & 0xFF == ord("q"):
    #        break
    # cv2.destroyAllWindows()


#thread1 = camThread("camera", 4)
#thread1.start()