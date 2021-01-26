from threading import Thread
import cv2
import vision
import pyrealsense2

class DistanceGet:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self):
        self.frames = None
        self.stopped = False
        self.x = 0
        self.y = 0
        self.w = 0
        self.h = 0
        self.distance = None
        self.average = [0] * 5
        self.dist_prev = None

    def start(self):
        Thread(target=self.getDist, args=()).start()
        return self

    def getDist(self):
        while not self.stopped:

            if self.x != 0:
                depth_frame = self.frames.get_depth_frame()
                count = 0
                total = 0
                distprev = 0
                try:
                    pass
                    # meaure the distance of every pixel of the blob size on half of its height throughout it's width
                    for z in range(int(self.w)):
                        for i in range(int(20)):
                            dist = depth_frame.get_distance(self.x + z, int(self.y/2) + i)
                            #print(dist)
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
                    self.distance = (total / count)
                    print(self.distance)

                    # print(self.x, self.y, self.w, self.h)
                    # # print(video_getter.distance)
                    # # print(video_getter.x, video_getter.y, video_getter.w, video_getter.h)
                    # if dist < 1.33 * self.dist_prev or dist > 0.67 * self.dist_prev or 0 in self.average:
                    #     self.average.append(dist)
                    #     self.distance = sum(self.average) / len(self.average)
                    #     self.dist_prev = dist
                    # else:
                    #     print("värdmõõt" + str(dist))
                except:
                    # print("Error in measuring distance from pixel")
                    pass

    def stop(self):
        self.stopped = True