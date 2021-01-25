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
from videoGet2 import imageCapRS2
from realsense_config import activate_rs_settings
from InfoGet import BallGet
width = 1280
height = 720

kernel=np.ones((4, 4), np.uint8)

keskmistamine = [0] * 30
dist_prev = 0

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

#video_getter = VideoGet(4).start()
#first_frame = video_getter.frame
activate_rs_settings()
video_getter = imageCapRS2()
first_frame = video_getter.currentFrame


while True:

    if video_getter.stopped:
        video_getter.stop()
        break
    try:
        bgr = video_getter.currentFrame
        hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
        #cv2.imshow("bgr", bgr)
        #cv2.imshow("hsv", hsv)
        aabits = video_getter.depth_color_image
        #if video_getter.depth_color_frame is not None:
        cv2.imshow("depth",aabits)
        # 1. OpenCV gives you a BGR image
        #_, bgr = cam.read()
        #cv2.imshow("bgr", bgr)
        # 2. Convert BGR to HSV where color distributions are better
        #cv2.imshow("hsv", hsv)
        #masked_img = cv2.inRange(hsv, (filters["min"]), (filters["max"]))
        masked_img = cv2.inRange(hsv, saved_color["min"], saved_color["max"])
        kernel = np.ones((5, 5), np.uint8)
        masked_img2 = cv2.morphologyEx(masked_img, cv2.MORPH_OPEN, kernel)
        erosion = cv2.erode(masked_img2, kernel, iterations=1)
        dilation = cv2.dilate(erosion, kernel, iterations=1)
        cont, hie = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Get blob contour coordinates
        cnt = cont[0]
        x, y, w, h = cv2.boundingRect(cnt)
        print(y+h)
        # Draw bounding rect to pic
        cv2.rectangle(hsv, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # update dist getter coordinates
        video_getter.set_coordinates(x, y, w, h)
        dist = video_getter.get_distance()
        #print(video_getter.distance)
        #print(video_getter.x, video_getter.y, video_getter.w, video_getter.h)
        if dist < 1.33 * dist_prev or dist > 0.67 * dist_prev or 0 in keskmistamine:
            keskmistamine.append(dist)
            keskmistamine.pop(0)
            #print(sum(keskmistamine)/len(keskmistamine))
            dist_prev = dist
        else:
            #print("värdmõõt" + str(dist))
            pass

        # try:
        #     cnt = cont[0]
        #     x, y, w, h = cv2.boundingRect(cnt)
        #     print(y+h)
        #     cv2.rectangle(hsv, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #except:
        #    pass

        cv2.imshow("haesve", hsv)
        contour_img = cv2.drawContours(masked_img2, cont, -1, (255, 0, 255))



        try:
            max_cont = max(cont, key=cv2.contourArea)
            (x, y), r = cv2.minEnclosingCircle(max_cont)
            x = int(x)
            y = int(y)
            r = int(r)
            #print(y)
            # print("vision color filter: ", (x, y), r)

        except Exception as e:
            # print("Nothing found, returning 0, 0, 0")
            x = None;
            y = None;
            r = None


        #cv2.imshow("bgr", r)
        cv2.imshow("cont", contour_img)

    except:
        pass

    key = cv2.waitKey(10)

    if key & 0xFF == ord("s"):
        save()

    if key & 0xFF == ord("q"):
        video_getter.stop()
        save()
        break

