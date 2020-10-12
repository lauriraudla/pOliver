import cv2
import json
from pOliver import omni_movement, vision_test

kernel = 3

try:
    with open("colors.json", "r") as f:
        saved_colors = json.loads(f.read())
except FileNotFoundError:
    saved_colors = {}

color = "green"

right = 'sd:7:7:7 \n'
left = 'sd:-7:-7:-7 \n'
brrr = 'sd:10:10:10 \n'
stop = 'sd:0:0:0 \n'

#ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

if color in saved_colors:
    filters = saved_colors[color]
else:
    filters = {
        "min": [0, 0, 0], # HSV minimum values
        "max": [179, 255, 255] # HSV maximum values
    }

#blobdetector
blobparams = cv2.SimpleBlobDetector_Params()
blobparams.filterByColor = False
blobparams.filterByConvexity = False
blobparams.filterByInertia = False
blobparams.filterByArea = True
blobparams.minArea = 50
blobparams.maxArea = 10000
blobparams.minDistBetweenBlobs = 4000
detector = cv2.SimpleBlobDetector_create(blobparams)

cap = vision_test.imageCapRS2()

while True:
    # 1. OpenCV gives you a BGR image
    bgr = cap.getFrame()
    #cv2.imshow("bgr", bgr)
    # 2. BGR -> HSV
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    #cv2.imshow("hsv", hsv)
    hsv = cv2.blur(hsv, (kernel, kernel))
    # 3. Use filters on HSV image
    mask = cv2.inRange(hsv, tuple(filters["min"]), tuple(filters["max"]))

    kp = detector.detect(mask)
    pt = cv2.KeyPoint_convert(kp)
    #width 640
    try:
        ball = pt[0][0]
        if ball < 280:
            print("right go brrrrrrrrrr")
            #ser.write(right.encode())
            omni_movement.turnRight()
            #right
        elif ball > 360:
            print("left go brrrrrrrrrr")
            #ser.write(left.encode())
            omni_movement.turnLeft()
            #left
        else:
            print("else")
            omni_movement.omni_move(12, -90)
            #ser.write(stop.encode())

    except:
        print("spin go brrrrrrrrr")
        omni_movement.turnFast()
        # suurem pööre

    #while (ser.inWaiting()):
        #print(ser.read())

    for x in pt:
        cv2.putText(mask, (str(x[0]) + " " + str(x[1])), (int(x[0]), int(x[1])), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (200, 50, 69), 2)

    cv2.imshow("mask", mask)

    key = cv2.waitKey(10)
    if key & 0xFF == ord("q"):
        cap.setStopped(False)
        break

cv2.destroyAllWindows()
