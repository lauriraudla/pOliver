import argparse
import os
import cv2
from CountsPerSec import CountsPerSec
from VideoGet import VideoGet
from InfoGet import BallGet
from ref import Referee
import omni2
import time
import websocket
import LUT
from videoGet2 import imageCapRS2
from realsense_config import activate_rs_settings
from distanceFinder import DistanceGet

go = False
robot = "pOliver"
# Testvõistluse server
#ws = websocket.create_connection('ws://192.168.2.220:8111/')
# Server Sveni läpakas
#ws = websocket.create_connection('ws://192.168.2.64:8887/')
# Server Punamütsike
ws = websocket.create_connection('ws://192.168.2.13:8887/')

def threadBoth():
    global go
    global robot
    global ws

    ref = Referee(ws).start()
    video_getter = imageCapRS2() # muutujatena antakse mõõdetava punkti kaugus
    first_frame = video_getter.currentFrame
    info_shower = BallGet(first_frame).start()
    distance_finder = DistanceGet().start()

    integral = 0
    derivative = 0
    err_prev = 0
    err_prev_fwd = 0
    err_prev_rot = 0
    errors_array = [0] * 40
    dummy_errors_array = [0] * 40
    flag = 0
    driveState = 0
    thrown = False


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

    errors_array = [0] * 40
    dummy_errors_array = [0] * 40
    flag = 0
    go = ref.go

    while True:
        # Kontrollib, kas mõni thread on seisma pandud ja paneb ka teised seisma
        if video_getter.stopped or info_shower.stopped or ref.stopped or distance_finder.stopped:
            info_shower.stop()
            video_getter.stop()
            ref.stop()
            distance_finder.stop()
            omni2.stopAll(values)
            cv2.destroyAllWindows()
            break
        #Uuendame kaadrit, krovi ja palli infot
        frame = video_getter.currentFrame
        # info_shower.basket = False
        info_shower.frame = frame
        ball = info_shower.info
        korv = info_shower.info2
        distance_finder.info = korv
        distance_finder.frame = video_getter.frames
        distance_finder.set_coordinates(korv[0], korv[1], korv[4], korv[5])
        go = ref.go


        # kui kohtunikult on tulnud start käsklus
        if go:
            try:
                if ball[0] is not None and ball[1] > 20:
                    if ballFind == True:
                        omni2.stopAll(values)
                        #time.sleep(0.2)
                        ballFind = False
                    x = ball[0]
                    y = ball[1]
                    # print(ball)
                    if korv[0] is not None:
                        # print(flag,x,y)
                        if flag == 0:
                            if driveState != 2:
                                integral = 0
                                derivative = 0
                                err_prev = 0
                                driveState = 2
                            # print("türa")
                            omni2.ballRotate(values,
                                             -1 * omni2.pidBallCenterRotateSpeed(korv[0], integral, derivative,
                                                                                 err_prev_rot, errors_array),
                                             omni2.pidBallCenter(x, integral, derivative, err_prev),
                                             omni2.pidBallCenterForward(y, integral, derivative, err_prev_fwd))

                        if all(abs(n) < 20 for n in errors_array) and y > 540 or flag == 1:
                            flag = 1
                            print("alustan viskamist")
                            # print(y)
                            if y < 690:
                                print("lammas")
                                omni2.ballRotate(values,
                                                 -1 * omni2.pidBallCenterRotateSpeed(korv[0], integral, derivative,
                                                                                     err_prev_rot, dummy_errors_array),
                                                 omni2.pidBallCenter(x, integral, derivative, err_prev),
                                                 -5)
                            else:
                                print("lehm")

                                x = 0
                                omni2.stopAll(values)
                                time.sleep(0.1)
                                # thrower_average = [int(int(LUT.get_thrower_speed(korv[1]))*0.93)] * 20
                                omni2.startThrow(values, int(int(LUT.get_thrower_speed(korv[1])) * 0.89) + 5)
                                while x < 2500:
                                    integral = 0
                                    derivative = 0
                                    err_prev = 0
                                    omni2.forward(values,7)
                                    recv = omni2.returnRecv()
                                    if recv == 1 and not thrown:
                                        x = 2475
                                        thrown = True
                                    x -= -1
                                thrown = False
                                flag = 0
                                omni2.endThrow(values)
                    # kui pall on kaugemal kui väärtus
                    elif y < 60 and y is not None and y != 0:
                        # print(1)
                        if driveState != 0:
                            integral = 0
                            derivative = 0
                            err_prev = 0
                            driveState = 0
                        pid = omni2.pid2(x, integral, derivative, err_prev)
                        omni2.toBall(values, 15, [pid, y])
                    elif y < 230 and y is not None and y != 0:
                        # print(1)
                        pid = omni2.pid2(x, integral, derivative, err_prev)
                        omni2.toBall(values, 55, [pid, y])
                        # kui pall on kaugemal kui väärtus
                        # print("uss")
                    elif y < 440 and y is not None and y != 0:
                        # print(1)
                        pid = omni2.pid2(x, integral, derivative, err_prev)
                        omni2.toBall(values, 25, [pid, y])
                        # print("lammas")
                    elif y > 440 and y is not None and y != 0:
                        # print(1)
                        # print(ball)
                        if driveState != 1:
                            integral = 0
                            derivative = 0
                            err_prev = 0
                            driveState = 1
                        omni2.ballRotate(values,
                                         -1 * omni2.pidBallCenterRotateSpeed(korv[0], integral, derivative,
                                                                             err_prev_rot, errors_array),
                                         omni2.pidBallCenter(x, integral, derivative, err_prev),
                                         omni2.pidBallCenterForward(y, integral, derivative, err_prev_fwd))
                        # print(errors_array)

                else:
                    print("otsin")
                    ballFind = True
                    omni2.rotate(values, 7)
                    #time.sleep(0.3)
                    integral = 0
                    derivative = 0
                    err_prev = 0
            except:
                ballFind = True
                print("otsin2")
                omni2.rotate(values, 7)
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