# GOALS:
# 1. Show webcam
# 2. Filter ball color
# 2.a. Maybe try HSV instead of RGB
# 3. Done


import cv2
import json
from functools import partial
import numpy as np
from VideoGet import VideoGet
import config
#from pOliver import vision_test, image_thread

width = 1280
height = 720

kernel=np.ones((4, 4), np.uint8)

# Load saved color values from colors.json

#print("Saved color values: ", saved_colors)
color = input("What color to threshold: ")
try:
    with open("config.ini", "r") as f:
        saved_color = config.get("colors", color)
        print(saved_color)
except FileNotFoundError:
    saved_color = {}



# Read color values from colors.json or initialize new values
if saved_color == config.get("colors", color):
    filters = saved_color
    print(filters["min"])
    print(filters["min"][1])
else:
    filters = {
        "min": (0, 0, 0), # HSV minimum values
        "max": (255, 255, 255) # HSV maximum values
    }

def save():
    config.set("colors", color, filters)
    config.save()


def update_range(i, j, value):
    values = list(saved_color[i])
    values[j] = value
    saved_color[i] = tuple(values)


cv2.namedWindow("frame")

cv2.createTrackbar("h_min", "frame", saved_color["min"][0], 255, partial(update_range, "min", 0))
cv2.createTrackbar("s_min", "frame", saved_color["min"][1], 255, partial(update_range, "min", 1))
cv2.createTrackbar("v_min", "frame", saved_color["min"][2], 255, partial(update_range, "min", 2))
cv2.createTrackbar("h_max", "frame", saved_color["max"][0], 255, partial(update_range, "max", 0))
cv2.createTrackbar("s_max", "frame", saved_color["max"][1], 255, partial(update_range, "max", 1))
cv2.createTrackbar("v_max", "frame", saved_color["max"][2], 255, partial(update_range, "max", 2))

video_getter = VideoGet(4).start()
first_frame = video_getter.frame

while True:

    if video_getter.stopped:
        video_getter.stop()
        break

    hsv = video_getter.frame
    # 1. OpenCV gives you a BGR image
    #_, bgr = cam.read()
    #cv2.imshow("bgr", bgr)

    # 2. Convert BGR to HSV where color distributions are better
    #hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    #cv2.imshow("hsv", hsv)
    #masked_img = cv2.inRange(hsv, (filters["min"]), (filters["max"]))
    masked_img = cv2.inRange(hsv, saved_color["min"], saved_color["max"])
    kernel = np.ones((5, 5), np.uint8)
    masked_img = cv2.morphologyEx(masked_img, cv2.MORPH_OPEN, kernel)
    erosion = cv2.erode(masked_img, kernel, iterations=1)
    dilation = cv2.dilate(erosion, kernel, iterations=1)
    cont, hie = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contour_img = cv2.drawContours(masked_img, cont, -1, (255, 0, 255))

    try:
        max_cont = max(cont, key=cv2.contourArea)
        (x, y), r = cv2.minEnclosingCircle(max_cont)
        x = int(x)
        y = int(y)
        r = int(r)
        # print("vision color filter: ", (x, y), r)

    except Exception as e:
        # print("Nothing found, returning 0, 0, 0")
        x = None;
        y = None;
        r = None


    #cv2.imshow("bgr", r)
    cv2.imshow("cont", contour_img)

    key = cv2.waitKey(10)

    if key & 0xFF == ord("s"):
        save()

    if key & 0xFF == ord("q"):
        video_getter.stop()
        save()
        break

