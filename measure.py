from VideoGet import VideoGet
from InfoGet import BallGet
import omni2
import cv2

width = 0
speed = 72
values = [25, 25, 0, 65, 65, 65, 0, 170]
# blue or magenta
color = "blue"

video_getter = VideoGet(4).start()
first_frame = video_getter.frame
info_shower = BallGet(first_frame).start()
omni2.startThrow(values, speed)

while True:
    try:
        if video_getter.stopped or info_shower.stopped:
            info_shower.stop()
            video_getter.stop()
            omni2.stopAll(values)
            break


        frame = video_getter.frame
        info_shower.frame = frame
        korv = info_shower.info2


        print("iks: " + str(korv[0]))
        print("ygrek: " + str(korv[1]))
        print("laius: " + str(korv[2]))
        print("summa: " + str(korv[1] + korv[2]))
        print()

    except:
        print("noob")
        pass

