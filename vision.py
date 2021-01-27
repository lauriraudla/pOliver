import cv2
import numpy as np
import config

# Get color ranges and noise removal kernels from config
ball_color_range = config.get("colors", config.get("vision", "ball_color"))
ball_noise_kernel = config.get("vision", "ball_noise_kernel")
# basket_color_range = config.get("colors", config.get("vision", "basket_color"))
edge_color_range = config.get("colors", config.get("vision", "bounds"))


def apply_ball_color_filter(hsv, basket=False, bounds = False, korv=None, piir=None):
    #print(ball_color_range)
    #print(hsv)
    height = 0
    w, h, x2, y2 = 0,0,0,0

    basket_color_range = config.get("colors", config.get("vision", "basket_color"))

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
        #cv2.imshow("hsv", hsv)
        #print(basket_color_range["min"], basket_color_range["max"])
    elif bounds:
        masked_img = cv2.inRange(hsv, edge_color_range["min"], edge_color_range["max"])
        pass
    else:
        masked_img = cv2.inRange(hsv, ball_color_range["min"], ball_color_range["max"])
        #print(ball_color_range["min"], ball_color_range["max"])
    kernel = np.ones((5, 5), np.uint8)
    masked_img2 = cv2.morphologyEx(masked_img, cv2.MORPH_OPEN, kernel)
    erosion = cv2.erode(masked_img2, kernel, iterations=1)
    dilation = cv2.dilate(erosion, kernel, iterations=1)
    cont, hie = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Get blob contour coordinates
    try:
        cnt = max(cont, key=cv2.contourArea)
        x2, y2, w, h = cv2.boundingRect(cnt)
        # Draw bounding rect to pic
        height = y2+h
        cv2.rectangle(hsv, (x2, y2), (x2 + w, y2 + h), (0, 255, 0), 2)
    except:
        #print("unable to draw contours")
        pass

    contour_img = cv2.drawContours(masked_img2, cont, -1, (255, 0, 255))
    # print("cont", cont)
    try:
        max_cont = max(cont, key=cv2.contourArea)
        (x, y), r = cv2.minEnclosingCircle(max_cont)
        x = int(x)
        y = int(y)
        r = int(r)
        # print("vision color filter: ", (x, y), r)
        print(korv)
        if korv is not None and korv > 190:
            print("liiga lähedal")
            x = None;
            y = None;
            r = None
            w = None
            h = None
            x2 = None
            y2 = None
        count = 0
        if piir is not None:
            try:
                for i in range(len(piir)-y):
                    alla = piir[y+i][x]
                    if alla > 0:
                        count += 1
                    elif alla == 0:
                        count = 0
                    if count == 7:
                        #print("pall on väljaspool")
                        x = None;
                        y = None;
                        r = None
                        w = None
                        h = None
                        x2 = None
                        y2 = None
                        count = 0
                        return x, y, r, contour_img
            except:
                pass

        if r < 3 and not basket:
            raise NotImplementedError
        if r < 10 and basket:
            raise NotImplementedError
    except Exception as e:
        # print("Nothing found, returning 0, 0, 0")
        x = None;
        y = None;
        r = None
        w = None
        h = None
        x2 = None
        y2 = None

    # Only return the blob of the largest objects of the same color
    #print(x,y)
    return x, y, r, contour_img, w, h, height, x2, y2


