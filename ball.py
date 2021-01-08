import cv2
import json
import numpy as np
import omni_movement
import time

kernel1 = np.ones((4,4), np.uint8)
kernel = 3
#Video resolution
width = 1280
height = 720


try:
    with open("colors.json", "r") as f:
        saved_colors = json.loads(f.read())
except FileNotFoundError:
    saved_colors = {}

color = "green"

state = 0

#ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

if color in saved_colors:
    filters = saved_colors[color]
else:
    filters = {
        "min": [0, 0, 0], # HSV minimum values
        "max": [255, 255, 255] # HSV maximum values
    }
green = saved_colors["green"]

# Start video capture
cam = cv2.VideoCapture(4)
cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
cam.set(cv2.CAP_PROP_EXPOSURE, 120.0)
cam.set(cv2.CAP_PROP_AUTO_WB, 0)
cam.set(cv2.CAP_PROP_WB_TEMPERATURE, 5700)
cam.set(3, width)
cam.set(4, height)

fps = 0
time0 = 0
time1 = 0

while True:


    # 1. OpenCV gives you a BGR image
    _, bgr = cam.read()
    time1 = time0
    time0 = time.time()
    fps = 1/(time0 - time1)
    print(fps)
    # 2. Convert BGR to HSV where color distributions are better
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    # 2.1 Cut out bottom of frame
    #cut = hsv[0:800][0:400]
    #findBall(cut,green)
    # 3. apply blur
    blur = cv2.blur(hsv, (3, 3))
    # 4. Use filters on HSV image
    mask = cv2.inRange(blur, tuple(filters["min"]), tuple(filters["max"]))
    bilateral = cv2.bilateralFilter(mask, 5, 175, 175)
    # 5. morphological actions
    opened = cv2.morphologyEx(bilateral, cv2.MORPH_OPEN, kernel1)
    # detect circles
    circles = cv2.HoughCircles(opened,
                               cv2.HOUGH_GRADIENT_ALT,
                               1,
                               minDist=200,
                               param1=300,
                               param2=0.3,
                               minRadius=1,
                               maxRadius=75)
    # draw circles
    if circles is not None:
        pt = np.round(circles[0, :]).astype("int")
        for (x, y, r) in pt:
            cv2.circle(bgr, (x, y), r, (0, 255, 0), 4)

    #cv2.imshow("mask", hsv)
    cv2.imshow("bgr", bgr)


    pt = circles
    try:
        print(pt)
        ball = pt[0][0][0]
        height = pt[0][0][1]
        print(ball)
        if ball < 580:
            print("right go brrrrrrrrrr")
            #ser.write(right.encode())
            if state != 1:
                omni_movement.turnRight()
                state = 1
            #right
        elif ball > 700:
            print("left go brrrrrrrrrr")
            #ser.write(left.encode())
            if state != 2:
                omni_movement.turnLeft()
                state = 2
            #left
        else:
            #print("else")
            try:
                # dist = cap.getDistance(int(pt[0][0]), int(pt[0][1]))
                # print(dist)
                if height < 380:
                    #omni_movement.omni_move(40, -90)
                    if state != 3:
                        omni_movement.stop()
                        state = 3
                        print("if")
                else:
                    if state != 4:
                        omni_movement.stop()
                        state = 4
                    #omni_movement.omni_move(0, -90)
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

    #cv2.imshow("tresh", opened)
    key = cv2.waitKey(10)
    if key & 0xFF == ord("q"):
        omni_movement.stop()
        break

cv2.destroyAllWindows()
