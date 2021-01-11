import argparse
import os
import cv2
from CountsPerSec import CountsPerSec
from VideoGet import VideoGet
from InfoGet import BallGet
from ref import Referee
import omni2
import time
import json
import websocket
import config
from _thread import *  # low level threading library
go = 0
robot = "pOliver"
ws = websocket.create_connection('ws://192.168.2.64:8887/')

def putIterationsPerSec(frame, iterations_per_sec):
    """
    Add iterations per second text to lower-left corner of a frame.
    """

    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame

def refereecomm(socket):
    print()

def threadBoth():
    global go
    global robot
    global ws


    ref = Referee(ws).start()
    video_getter = VideoGet(4).start()
    first_frame = video_getter.frame
    info_shower = BallGet(first_frame).start()
    integral = 0
    derivative = 0
    err_prev = 0
    go = ref.go


    #prev_img = []
    # basket_shower = BasketGet(first_frame2).start()
    state = 0# 0 otsib palli, 1 pöörleb, -> otsib korvi, -> 2 võtab palli keskele ja viskab

    cps = CountsPerSec().start()

    values = [25, 25, 0, 65, 55, 65, 0, 170]

    while True:



        if video_getter.stopped or info_shower.stopped or ref.stopped:
            info_shower.stop()
            video_getter.stop()
            ref.stop()
            omni2.stopAll(values)
            break

        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())
        info_shower.basket = False
        info_shower.frame = frame
        ball = info_shower.info
        korv = info_shower.info2
        #border = info_shower.info3
        go = ref.go
        #print(go)

        if go:
            try:
                if ball[0] is not None:
                    x = ball[0]
                    y = ball[1]
                    #print(ball)

                    # kui pall on kaugemal kui väärtus
                    if y < 60 and y is not None and y != 0:
                        pid = omni2.pid2(x, integral, derivative, err_prev)
                        omni2.toBall(values, 15, [pid, y])
                    elif y < 230 and y is not None and y != 0:
                        pid = omni2.pid(x, integral, derivative, err_prev)
                        omni2.toBall(values, 55, [pid, y])
                        # kui pall on kaugemal kui väärtus
                    elif y < 600 and y is not None and y != 0:
                        pid = omni2.pid2(x, integral, derivative, err_prev)
                        omni2.toBall(values, 25, [pid, y])
                    elif y > 600 and y is not None and y != 0:
                        omni2.ballRotate(values, 10, omni2.pidBallCenter(x, integral, derivative, err_prev))
                        #print(x)
                        try:
                            if 640 < korv[0] < 700:
                                omni2.stop(values)
                                omni2.startThrow(values, 100)
                                time.sleep(0.2)
                                omni2.forward(values, 15)
                                time.sleep(0.9)
                                omni2.endThrow(values)
                                integral = 0
                                derivative = 0
                                err_prev = 0
                        except:
                            #print("fail")
                            pass

                else:
                    # print("otsin")
                    omni2.rotate(values, 10)
                    integral = 0
                    derivative = 0
                    err_prev = 0
            except:
                #print("otsin")
                omni2.rotate(values,10)
                # kui palli ei ole keeruta koha peal
            cps.increment()
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