import argparse
import os
import cv2
from InfoGet import BallGet
from ref import Referee
import omni2
import time
import websocket
import LUT
from videoGet2 import imageCapRS2
from realsense_config import activate_rs_settings
import numpy as np

go = False
robot = "pOliver"
# Testvõistluse server
#ws = websocket.create_connection('ws://192.168.2.220:8111/')
# Server Sveni läpakas
ws = websocket.create_connection('ws://192.168.2.64:8887/')
# Server Punamütsike
#ws = websocket.create_connection('ws://192.168.2.13:8887/')

def threadBoth():
    global go
    global robot
    global ws

    ref = Referee(ws).start()
    video_getter = imageCapRS2() # muutujatena antakse mõõdetava punkti kaugus
    first_frame = video_getter.currentFrame
    frame = video_getter.currentFrame
    info_shower = BallGet(first_frame).start()

    integral = 0
    derivative = 0
    intFWS = 0
    intFWF = 0
    intRWS = 0
    derFWS = 0
    derFWF = 0
    derRWS = 0
    err_prev = 0
    err_prev_fwd = 0
    err_prev_rot = 0
    driveState = 0
    thrown = False

    speeds = []

    # Nullib kõik mainboardi PIDi, et ei hakkaks varasemast käima jäänud koodiga laamendama.
    values = [0, 0, 0, 0, 0, 0, 0, 170]
    omni2.sendIt(values)
    time.sleep(0.1)
    omni2.sendIt(values)
    time.sleep(0.1)
    omni2.sendIt(values)
    time.sleep(0.1)
    omni2.sendIt(values)
    time.sleep(0.1)
    omni2.sendIt(values)
    time.sleep(0.1)

    # Mainboardile saadetav kiiruste muutujaid sisaldav array
    values = [10, 8, 0, 65, 65, 65, 0, 170]

    activate_rs_settings()

    errors_array = [99] * 100
    dummy_errors_array = [99] * 100
    flag = 0
    go = ref.go
    #go = True
    last_x = 0

    rot_speed = 0
    rot_flag = 0

    driveState = None
    distances = []

    while True:
        # Kontrollib, kas mõni thread on seisma pandud ja paneb ka teised seisma
        if video_getter.stopped or info_shower.stopped or ref.stopped:
            info_shower.stop()
            video_getter.stop()
            ref.stop()
            omni2.stopAll(values)
            cv2.destroyAllWindows()
            break
        #Uuendame kaadrit, krovi ja palli infot
        #while video_getter.ready is True:
        ##print(time.time())
        frame = video_getter.currentFrame
        info_shower.frame = frame
        ball = info_shower.info
        korv = info_shower.info2
        video_getter.set_coordinates(korv[7], korv[8], korv[4], korv[5])
        go = ref.go


        # kui kohtunikult on tulnud start käsklus
        if go:
            try:
                if ball[0] is not None and ball[1] > 20:
                    if ballFind == True:
                        omni2.stopAll(values)
                        ballFind = False
                    x = ball[0]
                    y = ball[1]
                    # print(ball)
                    if korv[0] is not None:
                        if y < 400 and y is not None and y != 0:
                            pid = omni2.pid2(x, integral, derivative, err_prev)
                            omni2.toBall(values, 25, [pid, y])
                        elif flag == 0:
                            omni2.ballRotate(values,
                                             -1 * omni2.pidRearWheelSpeed(korv[0], errors_array),
                                             omni2.pidFrontWheelsSide(x),
                                             omni2.pidFrontWheelsforward(y))

                        if all(abs(n) < 20 for n in errors_array) or flag == 1:
                            flag = 1
                            #print("alustan viskamist")
                            if y < 600:
                                omni2.ballRotate(values,
                                                 -1 * omni2.pidRearWheelSpeed(korv[0], dummy_errors_array),
                                                 omni2.pidFrontWheelsSide(x),
                                                 -5)
                            else:
                                x = 0
                                omni2.stopAll(values)
                                time.sleep(0.1)
                                # Viskamine kasutades realsense'i
                                if len(distances) < 5:
                                    distance = video_getter.get_distance()
                                    if distance != 0:
                                        if distance is not None:
                                            distances.append(distance)
                                else:
                                    avg_distance = (sum(distances) / len(distances))
                                    speeds.append(avg_distance)
                                    distances = []
                                    avg_speed = (sum(speeds) / len(speeds))
                                    kiirus = LUT.get_thrower_speed(avg_speed)
                                    kiirus = int(kiirus * 1.01 + 1)
                                    print(kiirus)
                                    omni2.startThrow(values, kiirus)
                                    speeds = []
                                    # omni2.startThrow(values, int(int(LUT.get_thrower_speed(throw_dist))*1.1)-3)
                                    distances = []
                                    while x < 2500:
                                        korv = info_shower.info2
                                        omni2.ballRotate(values,
                                                         0,
                                                         0,
                                                         -3)
                                        recv = omni2.returnRecv()
                                        print(values)
                                        if recv == 1 and not thrown:
                                            x = 2475
                                            thrown = True
                                        x += 1
                                    print("vise lõppes")
                                    thrown = False
                                    print(errors_array)
                                    errors_array = [99] * 100
                                    dummy_errors_array = [99] * 100
                                    print(errors_array)
                                    flag = 0
                                    omni2.endThrow(values)

                    # elif y < 60 and y is not None and y != 0:
                    #     intRWS = 0
                    #     pid = omni2.pid2(x, integral, derivative, err_prev)
                    #     omni2.toBall(values, 40, [pid, y])
                    #
                    # elif y < 230 and y is not None and y != 0:
                    #     intRWS = 0
                    #     pid = omni2.pid2(x, integral, derivative, err_prev)
                    #     omni2.toBall(values, 45, [pid, y])
                    #
                    # elif y < 440 and y is not None and y != 0:
                    #     intRWS = 0
                    #     omni2.toBall(values, 15, [pid, y])

                    #elif y > 440 and y is not None and y != 0:
                    elif y < 400 and y is not None and y != 0:
                        pid = omni2.pid2(x, integral, derivative, err_prev)
                        omni2.toBall(values,25, [pid,y])
                    else:
                        intRWS = 0
                        omni2.ballRotate(values,
                                         -1 * omni2.pidRearWheelSpeed(None, errors_array),
                                         omni2.pidFrontWheelsSide(x),
                                         omni2.pidFrontWheelsforward(y))

                else:
                    #print("otsin")
                    ballFind = True
                    omni2.rotate(values, 7)
                    time.sleep(0.3)
                    omni2.reset("FWS")
                    omni2.reset("FWF")
                    omni2.reset("RWS")
                    integral = 0
                    derivative = 0
                    err_prev = 0
            except:
                ballFind = True
                #print("otsin2")
                omni2.rotate(values, 7)
                omni2.reset("FWS")
                omni2.reset("FWF")
                omni2.reset("RWS")
                integral = 0
                derivative = 0
                err_prev = 0
                # kui palli ei ole keeruta koha peal
        else:
            omni2.stopAll(values)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", "-s", default=4,
        help="Path to video file or integer representing webcam index"
            + " (default 0).")
    ap.add_argument("--thread", "-t", default="both",
        help="Threading mode: get (video read in its own thread),"
            + " show (video show in its own thread), both"
            + " (video read and video show in their own threads),"
            + " none (default--no multithreading)")
    args = vars(ap.parse_args())

    # If source is a string consisting only of integers, check that it doesn't
    # refer to a file. If it doesn't, assume it's an integer camera ID and
    # convert to int.
    if (
        isinstance(args["source"], str)
        and args["source"].isdigit()
        and not os.path.isfile(args["source"])
    ):
        args["source"] = int(args["source"])

    if args["thread"] == "both":
        threadBoth()


if __name__ == "__main__":
    main()