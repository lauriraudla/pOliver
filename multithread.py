import argparse
import os
import cv2
from CountsPerSec import CountsPerSec
from VideoGet import VideoGet
from VideoShow import VideoShow
import omni2
import time

def putIterationsPerSec(frame, iterations_per_sec):
    """
    Add iterations per second text to lower-left corner of a frame.
    """

    cv2.putText(frame, "{:.0f} iterations/sec".format(iterations_per_sec),
        (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255))
    return frame

def threadBoth(source=4):

    video_getter = VideoGet(source).start()
    video_shower = VideoShow(video_getter.frame).start()
    cps = CountsPerSec().start()

    values = [25, 25, 0, 65, 55, 65, 0, 170]
    while True:

        if video_getter.stopped or video_shower.stopped:
            video_shower.stop()
            video_getter.stop()
            omni2.stop(values)
            break
        frame = video_getter.frame
        frame = putIterationsPerSec(frame, cps.countsPerSec())
        video_shower.frame = frame
        info = video_shower.info
        try:
            x = info[0]
            y = info[1]
            pall = [x,y]
            if y < 200:
                if x < 540:
                    omni2.rotate(values, 2)
                elif x > 740:
                    omni2.rotate(values, -2)
                else:
                    omni2.forward(values, 25)

            elif y < 450:
                omni2.toBall(values,30,pall)
            else:
                try:
                    if x < 600:
                        omni2.rotate(values, 2)
                    elif x > 680:
                        omni2.rotate(values, -2)
                    else:
                        omni2.startThrow(values,60)
                        omni2.forward(values,10)
                        time.sleep(2)
                        omni2.endThrow(values)

                    #omni2.ballRotate(values,20)
                except:
                    print("puutsad")
                    pass

        except:
            print("spin go brrrrrrrrr")
            omni2.rotate(values, 10)
            # suurem pööre
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