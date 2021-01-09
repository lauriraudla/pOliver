import cv2
import numpy as np
from threading import currentThread
import config

# Get color ranges and noise removal kernels from config
ball_color_range = config.get("colors", config.get("vision", "ball_color"))
ball_noise_kernel = config.get("vision", "ball_noise_kernel")
basket_color_range = config.get("colors", config.get("vision", "basket_color"))


def apply_ball_color_filter(hsv, basket=False):
    #print(ball_color_range)
    #print(hsv)
    """
        args:
            hsv image
        returns:
            1) masked image of the ball
            2) masked image of the basket
            3) [x, y] for the coordinates of the ball
            4) [x, y] for the coordinates of the basket
    """

    # hsv = cv2.blur(hsv, (2,2))
    #print(ball_color_range)
    if basket:
        masked_img = cv2.inRange(hsv, basket_color_range["min"], basket_color_range["max"])
    else:
        masked_img = cv2.inRange(hsv, ball_color_range["min"], ball_color_range["max"])
    kernel = np.ones((4, 4), np.uint8)
    masked_img = cv2.morphologyEx(masked_img, cv2.MORPH_OPEN, kernel)
    erosion = cv2.erode(masked_img, kernel, iterations=1)
    dilation = cv2.dilate(erosion, kernel, iterations=1)
    # erosion = cv2.erode(masked_img, kernel, iterations=1)
    # dilation = cv2.dilate(erosion, kernel, iterations=1)
    # dilation = masked_img
    cont, hie = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # print("cont", cont)
    try:
        max_cont = max(cont, key=cv2.contourArea)
        (x, y), r = cv2.minEnclosingCircle(max_cont)
        x = int(x)
        y = int(y)
        r = int(r)
        # print("vision color filter: ", (x, y), r)

        if r < 3 and not basket:
            raise NotImplementedError
        if r < 10 and basket:
            raise NotImplementedError
    except Exception as e:
        # print("Nothing found, returning 0, 0, 0")
        x = None;
        y = None;
        r = None

    """hsv = cv2.medianBlur(hsv, 5)
    masked_img = cv2.inRange(hsv, ball_color_range["min"], ball_color_range["max"])
    mask_basket = cv2.inRange(hsv, basket_color_range["min"], basket_color_range["max"])
    kernel = np.ones(7) #11
    masked_img = cv2.morphologyEx(masked_img, cv2.MORPH_OPEN, kernel)
    mask_basket = cv2.morphologyEx(mask_basket, cv2.MORPH_OPEN, kernel)"""
    # Only return the blob of the largest objects of the same color

    return x, y, r, dilation


