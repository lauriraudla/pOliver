# GOALS:
# 1. Show webcam
# 2. Filter ball color
# 2.a. Maybe try HSV instead of RGB
# 3. Done


import cv2
import json
from functools import partial
import numpy as np
#from pOliver import vision_test, image_thread

width = 1280
height = 720

kernel=np.ones((4, 4), np.uint8)

# Load saved color values from colors.json
try:
    with open("colors.json", "r") as f:
        saved_colors = json.loads(f.read())
except FileNotFoundError:
    saved_colors = {}

print("Saved color values: ", saved_colors)
color = input("What color to threshold: ")

# Read color values from colors.json or initialize new values
if color in saved_colors:
    filters = saved_colors[color]
else:
    filters = {
        "min": [0, 0, 0], # HSV minimum values
        "max": [255, 255, 255] # HSV maximum values
    }

def save():
    saved_colors[color] = filters

    with open("colors.json", "w") as f:
        f.write(json.dumps(saved_colors))

def update_range(edge, channel, value):
    # edge = "min" or "max"
    # channel = 0, 1, 2 (H, S, V)
    # value = new slider value
    filters[edge][channel] = value

# Create sliders to filter colors from image
cv2.namedWindow("mask")

# createTrackbar(name, window name, initial value, max value, function to call on change)
cv2.createTrackbar("h_min", "mask", filters["min"][0], 255, partial(update_range, "min", 0))
cv2.createTrackbar("s_min", "mask", filters["min"][1], 255, partial(update_range, "min", 1))
cv2.createTrackbar("v_min", "mask", filters["min"][2], 255, partial(update_range, "min", 2))
cv2.createTrackbar("h_max", "mask", filters["max"][0], 255, partial(update_range, "max", 0))
cv2.createTrackbar("s_max", "mask", filters["max"][1], 255, partial(update_range, "max", 1))
cv2.createTrackbar("v_max", "mask", filters["max"][2], 255, partial(update_range, "max", 2))

# Start video capture
cam = cv2.VideoCapture(4)
cam.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
cam.set(cv2.CAP_PROP_EXPOSURE, 120.0)
cam.set(cv2.CAP_PROP_AUTO_WB, 0)
cam.set(cv2.CAP_PROP_WB_TEMPERATURE, 5700)
cam.set(3, width)
cam.set(4, height)

while True:
    # 1. OpenCV gives you a BGR image
    _, bgr = cam.read()
    #cv2.imshow("bgr", bgr)

    # 2. Convert BGR to HSV where color distributions are better
    hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
    #cv2.imshow("hsv", hsv)
    masked_img = cv2.inRange(hsv, tuple(filters["min"]), tuple(filters["max"]))
    kernel = np.ones((5, 5), np.uint8)
    masked_img = cv2.morphologyEx(masked_img, cv2.MORPH_OPEN, kernel)
    erosion = cv2.erode(masked_img, kernel, iterations=1)
    dilation = cv2.dilate(erosion, kernel, iterations=1)

    cv2.imshow("bgr", bgr)
    cv2.imshow("bilateral", dilation)

    key = cv2.waitKey(10)

    if key & 0xFF == ord("s"):
        save()

    if key & 0xFF == ord("q"):
        save()
        break

cam.release()
