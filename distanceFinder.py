from threading import Thread
import cv2
import vision

class DistanceGet:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, frames=None, info=None):
        self.frames = frames
        self.stopped = False
        self.info = info
        if info is not None:
            self.x = info[0]
            self.y = info[1]
            self.w = info[4]
            self.h = info[5]
        self.distance = None
        self.average = [0] * 5
        self.dist_prev = None

    def start(self):
        Thread(target=self.getDist(), args=()).start()
        return self

    def set_coordinates(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def getDist(self):
        while not self.stopped and self.info is not None:
            depth_frame = self.frames.get_depth_frame()
            color_frame = self.frames.get_color_frame()

            count = 0
            total = 0
            try:
                # meaure the distance of every pixel of the blob size on half of its height throughout it's width
                for z in range(self.w):
                    dist = depth_frame.get_distance(self.x + z, self.y + int(self.h / 2))
                    if dist == 0.0:
                        pass
                    else:
                        total += dist
                        count += 1
                # aritmethic average of all of the measurements
                self.distance = int(total / count)

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
                print("Error in measuring distance from pixel")
                pass

    def stop(self):
        self.stopped = True