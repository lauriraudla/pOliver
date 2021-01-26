from VideoGet import VideoGet
from InfoGet import BallGet
import omni2
import serial
import time
import cv2

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

width = 0
speed = 74
values = [25, 25, 0, 65, 65, 65, 0, 170]
# blue or magenta
color = "blue"

video_getter = VideoGet(4).start()
first_frame = video_getter.frame
info_shower = BallGet(first_frame).start()
#omni2.startThrow(values, speed)
read = 0
recv = 0
omni2.startThrow(values, speed)

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
            break


        frame = video_getter.frame
        info_shower.frame = frame
        korv = info_shower.info2
        print(korv[6],"korvi kõrgus")

        #print("iks: " + str(korv[0]))
        #print("ygrek: " + str(korv[1]))
        #print("laius: " + str(korv[2]))
        #print("summa: " + str(korv[1] + korv[2]))
        #print()

    except:
        #print("noob")
        pass

