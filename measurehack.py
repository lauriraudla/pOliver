from videoGet2 import imageCapRS2
import realsense_config
from InfoGet import BallGet
import omni2
import serial

try:
    ser = serial.Serial('/dev/ttyACM1', 115200, timeout=1)
except:
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

width = 0
speed = 10
values = [25, 25, 0, 65, 65, 65, 0, 170]
# blue or magenta
color = "blue"

realsense_config.activate_rs_settings()

video_getter = imageCapRS2()
first_frame = video_getter.currentFrame
info_shower = BallGet(first_frame).start()

read = 0
recv = 0
omni2.startThrow(values, speed)
speedarray = []
distarray = []
basketarray = []
korv = 0
distance = 0

while True:

    try:
        if video_getter.stopped or info_shower.stopped:
            info_shower.stop()
            video_getter.stop()
            omni2.stopAll(values)
            print(speedarray)
            print(distarray)
            break

        for x in range(5000):
            frame = video_getter.currentFrame
            info_shower.frame = frame
            korv = info_shower.info2
            video_getter.set_coordinates(korv[7], korv[8], korv[4], korv[5])
        distance = video_getter.get_distance()

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
                    distarray.append(distance)
                    basketarray.append(korv[0])
                    print(speedarray, "speed")
                    print(distarray, "dist")
                    print(basketarray, "basket")

        except:
            print("katki")
        print(speedarray, "speed")
        print(distarray, "dist")
        print(basketarray, "basket")


        omni2.startThrow(values,speed)

    except:
        print("noob")
        pass

