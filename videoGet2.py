import cv2
import pyrealsense2 as rs
import numpy as np
from threading import Thread
import math

class imageCapRS2:

    def commandThread(self):
        while not self.stopped:
            self.ready = False
            self.frames = self.pipeline.wait_for_frames()
            self.ready = True
            self.depth_frame = self.frames.get_depth_frame()
            self.color_frame = self.frames.get_color_frame()
            self.currentFrame = np.asanyarray(self.color_frame.get_data())
            #self.distance = self.get_distance()
            self.depth_color_frame = rs.colorizer().colorize(self.depth_frame)
            self.depth_color_image = np.asanyarray(self.depth_color_frame.get_data())

            # Aligning color frame to depth frame
            self.aligned_frames = self.align.process(self.frames)
            self.aligned_color_frame = self.aligned_frames.get_color_frame()

            if not self.depth_frame or not self.aligned_color_frame: continue

            self.color_intrin = self.aligned_color_frame.profile.as_video_stream_profile().intrinsics
            #depth_image = np.asanyarray(depth_frame.get_data())
            #color_image = np.asanyarray(aligned_color_frame.get_data())
            # Use pixel value of  depth-aligned color image to get 3D axes
            # if self.x is not None and self.y is not None:
            #     #x, y = 640, 360
            #     depth = self.depth_frame.get_distance(self.x,self.y)
            #     dx, dy, dz = rs.rs2_deproject_pixel_to_point(self.color_intrin, [self.x, self.y], depth)
            #     distance = math.sqrt(((dx) ** 2) + ((dy) ** 2) + ((dz) ** 2))
                #print("Distance from camera to pixel:", distance)
                #print("Z-depth from camera surface to pixel surface:", depth)

    def __init__(self, x=None, y=None):
        self.stopped = False
        self.depth_frame = None
        self.currentFrame = None
        self.depth_color_frame = None
        self.depth_color_image = None

        self.ready = False

        self.aligned_frames = None
        self.aligned_color_frame = None
        self.color_intrin = None

        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 60)
        self.config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 60)
        self.pipeline.start(self.config)

        self.align_to = rs.stream.depth
        self.align = rs.align(self.align_to)

        self.frames = self.pipeline.wait_for_frames()
        self.depth_frame = self.frames.get_depth_frame()
        self.color_frame = self.frames.get_color_frame()
        self.currentFrame = np.asanyarray(self.color_frame.get_data())
        self.depth_color_frame = rs.colorizer().colorize(self.depth_frame)
        self.depth_color_image = np.asanyarray(self.depth_color_frame.get_data())
        Thread(name="commandThread", target=self.commandThread).start()

        # Kauguse mõõtmine. x ja y on mõõdetava punkti koordinaadid depth mapil
        self.x = None
        self.y = None
        self.w = None
        self.h = None
        self.distance = None

    def getFrame(self):
        return self.depth_frame, self.currentFrame

    def stop(self):
        self.pipeline.stop()
        self.stopped = True

    def set_coordinates(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def get_distance(self):
        # x, y, width, height
        x = self.x
        y = self.y
        w = self.w
        h = self.h
        count = 0
        total = 0
        distprev = 0
        try:
            # meaure the distance of every pixel of the blob size on half of its height throughout it's width
            #for z in range(int(self.w/2)):
                #for i in range(int(self.h/2)):
                    #dist = self.depth_frame.get_distance(self.x + int(self.w/4) + z, int(self.y) + i)
            for z in range(int(self.w / 2)):
                for i in range(int(self.h / 2)):
                    dist = self.depth_frame.get_distance(self.x + int(self.w / 4) + z, int(self.y) + i)
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
            self.distance = round(total / count, 2)

            return self.distance
        except:
            print("Error in measuring distance from pixel")
            return 0.0
