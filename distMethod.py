
import pyrealsense2 as rs
def basketDist(depth_frame, x, y, w):
    count = 0
    total = 0
    distprev = 0
    if x is None:
        return None
        # meaure the distance of every pixel of the blob size on half of its height throughout it's width
    for z in range(int(w/2)):
        for i in range(int(10)):
            dist = depth_frame.get_distance(x + int(w/4) + z, int(y / 2) + i)
            # print(dist)
            if dist == 0.0:
                pass
            elif distprev == 0:
                distprev = dist
            elif dist > 1.2 * distprev:
                pass
            elif dist < 0.8 * distprev:
                pass
            else:
                total += dist
                count += 1
                distprev = dist
    # aritmethic average of all of the measurements
    if count == 0:
        return 0
    distance = (total / count)
    return distance