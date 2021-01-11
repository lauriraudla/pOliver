import argparse
import os
import cv2
from CountsPerSec import CountsPerSec
from VideoGet import VideoGet
from InfoGet import BallGet
from BasketGet import BasketGet
import omni2
import time
import copy

def putIterationsPerSec(frame, iterations_per_sec):
    """
    Add iterations per second text to lower-left corner of a frame.
    """

    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame

def threadBoth(source=4):

    video_getter = VideoGet(source).start()
    first_frame = video_getter.frame
    info_shower = BallGet(first_frame).start()
    integral = 0
    derivative = 0
    err_prev = 0
    # basket_shower = BasketGet(first_frame2).start()
    state = 0# 0 otsib palli, 1 pöörleb, -> otsib korvi, -> 2 võtab palli keskele ja viskab

    cps = CountsPerSec().start()

    values = [25, 25, 0, 65, 55, 65, 0, 170]

    while True:

        if video_getter.stopped or info_shower.stopped:
            info_shower.stop()
            video_getter.stop()
            omni2.stopAll(values)
            break

        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())
        info_shower.basket = False
        info_shower.frame = frame
        ball = info_shower.info
        korv = info_shower.info2

        try:
            if ball[0] is not None:
                x = ball[0]
                y = ball[1]
                # kui pall on kaugemal kui väärtus
                if y < 60:
                    pid = omni2.pid2(x, integral, derivative, err_prev)
                    omni2.toBall(values, 15, [pid, y])
                if y < 230:
                    pid = omni2.pid(x, integral, derivative, err_prev)
                    omni2.toBall(values, 55, [pid, y])
                    # kui pall on kaugemal kui väärtus
                elif y < 450:
                    pid = omni2.pid2(x, integral, derivative, err_prev)
                    omni2.toBall(values, 25, [pid, y])
                elif y > 450:
                    #integral, derivative, err_prev = 0
                    omni2.ballRotate(values, 10, omni2.pidBallCenter(x, integral, derivative, err_prev))
                    #omni2.stop(values)
                    print(x)
                    #omni2.ballRotateExact(values, 10)
                    # if x < 600:
                    #     omni2.Left(values)
                    # elif x > 680:
                    #     omni2.Right(values)
                    try:
                        #print("korv: " + str(korv[0]))
                        if 600 < korv[0] < 680:
                            omni2.startThrow(values, 100)
                            omni2.forward(values, 15)
                            time.sleep(0.7)
                            omni2.stopAll(values)
                    except:
                        print("fail")
                        pass

                else:
                    #print("otsin")
                    omni2.rotate(values, 3)
                    integral = 0
                    derivative = 0
                    err_prev = 0
        except:
            print("otsin")
            omni2.rotate(values,3)
            pass
            # kui palli ei ole keeruta koha peal
        cps.increment()

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
        threadBoth(args["source"])


if __name__ == "__main__":
    main()