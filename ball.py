import cv2
import json
import numpy as np
from pOliver import omni_movement, vision_test

kernel1 = np.ones((1,1), np.uint8)
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
        "max": [255, 255, 255] # HSV maximum values
    }
green = saved_colors["green"]
#blobdetector
# blobparams = cv2.SimpleBlobDetector_Params()
# blobparams.filterByColor = False
# blobparams.filterByConvexity = False
# blobparams.filterByInertia = False
# blobparams.filterByArea = True
# blobparams.minArea = 50
# blobparams.maxArea = 10000
# blobparams.minDistBetweenBlobs = 4000
# detector = cv2.SimpleBlobDetector_create(blobparams)

cap1 = vision_test.imageCapRS2()
cap = cv2.VideoCapture(cap1.getFrame())

# cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
# cap.set(cv2.CAP_PROP_EXPOSURE, 120.0)
# cap.set(cv2.CAP_PROP_AUTO_WB, 0)
# cap.set(cv2.CAP_PROP_WB_TEMPERATURE, 5700)
while True:
    # # 1. OpenCV gives you a BGR image
    # bgr = cap.getFrame()
    # #cv2.imshow("bgr", bgr)
    # # 2. BGR -> HSV
    # hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    # #cv2.imshow("hsv", hsv)
    # hsv = cv2.blur(hsv, (kernel, kernel))
    # # 3. Use filters on HSV image
    # mask = cv2.inRange(hsv, tuple(filters["min"]), tuple(filters["max"]))
    # # Old way of using random keypoints instead of circles
    # # kp = detector.detect(mask)
    # # pt = cv2.KeyPoint_convert(kp)
    # # 4. bilateral filtering on mask
    # bilateral = cv2.bilateralFilter(mask, 5, 175, 175)
    # # 4.1. opening morphology on filtered image
    # opened = cv2.morphologyEx(bilateral, cv2.MORPH_OPEN, kernel1)
    # # 5. Circle detection
    # circles = cv2.HoughCircles(opened, cv2.HOUGH_GRADIENT, 5, 100)
    # # 6. basing rest of the movement on the detected circles.
    # pt = circles
    #width 640

    # 1. OpenCV gives you a BGR image
    _, bgr = cap.read()
    # 2. Convert BGR to HSV where color distributions are better
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    # 2.1 Cut out bottom of frame
    cut = hsv[0:800][0:400]
    #findBall(cut,green)
    # 3. apply blur
    blur = cv2.blur(cut, (3, 3))
    # 4. Use filters on HSV image
    mask = cv2.inRange(blur, tuple(filters["min"]), tuple(filters["max"]))
    bilateral = cv2.bilateralFilter(mask, 5, 175, 175)
    # 5. morphological actions
    opened = cv2.morphologyEx(bilateral, cv2.MORPH_OPEN, kernel1)
    # detect circles
    circles = cv2.HoughCircles(opened, cv2.HOUGH_GRADIENT, 1, minDist=100, param1=400, param2=1, minRadius=3, maxRadius=50)
    # draw circles
    if circles is not None:
        pt = np.round(circles[0, :]).astype("int")
        for (x, y, r) in pt:
            cv2.circle(cut, (x, y), r, (0, 255, 0), 4)

    cv2.imshow("mask", cut)
    cv2.imshow("bgr", bgr)


    pt = circles
    try:
        print(pt)
        ball = pt[0][0][0]
        height = pt[0][0][1]
        print(ball)
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
            #print("else")
            try:
                # dist = cap.getDistance(int(pt[0][0]), int(pt[0][1]))
                # print(dist)
                if height < 300:
                    omni_movement.omni_move(40, -90)
                    print("if")
                else:
                    omni_movement.omni_move(0, -90)
                    print("else")
            except:
                print("puutsad")
                pass
            # #ser.write(stop.encode())

    except:
        print("spin go brrrrrrrrr")
        omni_movement.turnFast()
        # suurem pööre

    #while (ser.inWaiting()):
        #print(ser.read())

    #for x in pt:
    #    cv2.putText(mask, (str(x[0]) + " " + str(x[1])), (int(x[0]), int(x[1])), cv2.FONT_HERSHEY_SIMPLEX, 1,
    #               (200, 50, 69), 2)

    cv2.imshow("tresh", opened)
    key = cv2.waitKey(10)
    if key & 0xFF == ord("q"):
        cap.setStopped(False)
        break

cv2.destroyAllWindows()
