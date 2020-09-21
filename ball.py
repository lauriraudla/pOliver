import cv2
import json
import serial

kernel = 3

try:
    with open("colors.json", "r") as f:
        saved_colors = json.loads(f.read())
except FileNotFoundError:
    saved_colors = {}

color = "green"

left = 'sd:10:10:10 \n'
right = 'sd:-10:-10:-10 \n'
brrr= 'sd:25:25:25 \n'

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

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
blobparams.minArea = 100
blobparams.maxArea = 10000
blobparams.minDistBetweenBlobs = 4000
detector = cv2.SimpleBlobDetector_create(blobparams)

cap = cv2.VideoCapture(1)

while cap.isOpened():
    # 1. OpenCV gives you a BGR image
    _, bgr = cap.read()
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
        if ball < 290:
            print("right go brrrrrrrrrr")
            ser.write(right.encode())
            #right
        if ball > 350:
            print("left go brrrrrrrrrr")
            ser.write(left.encode())
            #left
    except:
        print("spin go brrrrrrrrr")
        ser.write(brrr.encode())
        #suurem pööre
    for x in pt:
        cv2.putText(mask, (str(x[0]) + " " + str(x[1])), (int(x[0]), int(x[1])), cv2.FONT_HERSHEY_SIMPLEX, 1,
                    (200, 50, 69), 2)

    cv2.imshow("mask", mask)

    key = cv2.waitKey(10)
    if key & 0xFF == ord("q"):
        break

cap.release()
