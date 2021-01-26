from videoGet2 import imageCapRS2
from InfoGet import BallGet
import omni2
import serial
import time
import cv2
from distanceFinder import DistanceGet

try:
    ser = serial.Serial('/dev/ttyACM1', 115200, timeout=1)
except:
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

width = 0
speed = 50
values = [25, 25, 0, 65, 65, 65, 0, 170]
# blue or magenta
color = "blue"

video_getter = imageCapRS2()
first_frame = video_getter.currentFrame
info_shower = BallGet(first_frame).start()

distance_finder = DistanceGet(first_frame).start()
print("dist_start")
#distance_finder.set_coordinates(0, 0, 0, 0)
#omni2.startThrow(values, speed)
read = 0
recv = 0
omni2.startThrow(values, speed)
speedarray = []
distarray = []

while True:

    try:
        #recv = omni2.returnRecv()
        #if recv == 1:
            #for x in range(2000):
            #    print("lendas!!!")
            #omni2.endThrow(values)
        # while ser.inWaiting():
        #     read = ser.read()
        #     #print(read[len(read)-2])
        # if read[len(read)-2] == 1:
        #     #print("sain 1")
        #     read = 0
        #     time.sleep(1)
        #     omni2.endThrow(values)
        if video_getter.stopped or info_shower.stopped:
            info_shower.stop()
            video_getter.stop()
            omni2.stopAll(values)
            print(speedarray)
            print(distarray)
            break

        for x in range(500):
            print(x)
            frame = video_getter.currentFrame
            info_shower.frame = frame
            korv = info_shower.info2

            distance_finder.depth_frame = video_getter.depth_frame
            distance_finder.set_coordinates(korv[7], korv[8], korv[4], korv[5])
            #print(korv[7], korv[8], korv[4], korv[5])
            distance = distance_finder.distance
            #print(distance)

        print(korv[6],"korvi kõrgus")
        print(distance, "realsense kaugus")
        inp = float(input("suuruse muut:"))
        if inp == 6.9:
            pass
        else:
            speed = speed+int(inp)
        try:
            if inp == 6.9:
                if korv[6] != 0:
                    speedarray.append(speed)
                    distarray.append(korv[6])

                    print(speedarray, "speed")
                    print(distarray, "speed")

        except:
            print("katki")
        print(speedarray,"speed")
        print(distarray,"speed")


        omni2.startThrow(values,speed)


        #print("iks: " + str(korv[0]))
        #print("ygrek: " + str(korv[1]))
        #print("laius: " + str(korv[2]))
        #print("summa: " + str(korv[1] + korv[2]))
        #print()

    except:
        print("noob")
        pass

