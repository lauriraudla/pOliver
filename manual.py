import cv2
import omni2

values = [25, 25, 0, 65, 65, 65, 0, 170]
thrower = 100
speed = 40

cv2.namedWindow("Controller")

while True:
    k = cv2.waitKey(1) & 0xFF

    if k == ord("w"):
        print("Forward")
        omni2.forward(values, speed)
    if k == ord("s"):
        print("Backward")
        omni2.forward(values, speed * -1)
    if k == ord("d"):
        print("Right")
        omni2.rotate(values, speed * -1)
    if k == ord("a"):
        print("Left")
        omni2.rotate(values, speed)
    if k == ord("t"):
        print("Throw")
        omni2.startThrow(values, thrower)
    if k == ord("r"):
        print("Stop throw")
        omni2.endThrow(values)
    if k == ord("e"):
        print("Stop")
        omni2.stopAll(values)
    if k == ord("q"):
        print("Break")
        omni2.stopAll(values)
        break

cv2.destroyAllWindows()
