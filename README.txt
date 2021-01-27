The code repository for team pOliver

Before running code install following modules(or make sure they are already installed):
cv2, pyrealsense2, websocket, json, serial, math, argparse, os, time, numpy, datetime, threading, ast, pathlib, configparser, functools
These are used for a variety of reasons -
configparser, json, ast, pathlib for getting values from the config file
websocket for referee handling, serial for writing to mainboard
numpy and math for doing math that isn't part of default python
cv2 and pyrealsense2 for image processing, distance measurement
threading is probably the most.. useful - create independent threads to run code - speeds up things A LOT. Potential downside = too many threads - python threads are smart enough to utilize physical threads, so the optimal number for a 2c4t processor is up to 4 threads

motortest.py is used for giving motors speed individually
For our specific robot, values are 
first 3 bytes are PID to be given to robot
next 3 values are for motors, between 0 and 130 for motor speeds, 65 being 0 speed, 0 and 130 being -65 and 65 respectively
next *number* values are for thrower control, between 0 and 130 for thrower speeds, no shenanigans here
last value being a control byte for the mainboard

thresh.py is used for thresholding the image, different colour values of green, blue, magenta and black
same values are used later.

With the robot now working and colours thresholded, start multithread2.py(!!change socket ip in the beginning of the file!!)
Send appropriate command via websocket to start/stop game logic. Basket colour can be changed when the logic section is running - can change basket mid round(good for testing purposes).
multithread2.py utilizes many included modules - InfoGet to process images, LUT.py for thrower speed, omni2.py for movement, realsense_config.py to make sure the camera has the right settings loaded, ref.py for referee handling, videoGet2 for frame aquirement and depth calculations, vision.py for thresholding images and returning appropriate values

measurehack.py creates a while loop, where it processes the images gotten from the image thread x times, at the end of the cycle prints out the distance(realsense), some basket information and asks for input - what to do with thrower speed? + and - integers to change speed, 6.9 is a *float* and a special case - add current speed and basket distance to lists, and print out said lists
Closing the program(q on the images, anything as input later) prints the full list of speeds/distances(/basket x location), for easy copying into LUT.py values. Fun fact: pressing enter without giving any input lets you quickly go through the for loop again for distance measurement - accidental feature from try-except!

Game logic:
if go is true, means we are currently in a round and the rest of the logic works
if there is no ball, spin
move to ball, depending on if a basket is visible use slightly different methods
if no basket, move around ball until found, 
when both basket and ball, get them both (near) the centre of the image, 
get close to the ball, take multiple measurements of distance and use that to get speed from LUT.py
throw ball - sensor can also detect ball being thrown to end throw early and get out of a lengthy while loop
after thrown, reset most of our  values and start cycle from the start

The overall code structure starts to resemble object oriented programming, where we want values of other objects, not values of methods. After declaring all the iterables and starting threads, we get to the while loop:
update image and image processing threads
perform game logic
repeat
there are some try-except pairs to help address situations where we try to use ball or basket info when there is none available
The threads run 100% separately from the main loop, we just use their values in the main loop to feed other threads new information. This form of threading allows us to reach ~300+ loop cycles a second, which is more than plenty to not bottleneck our code.
