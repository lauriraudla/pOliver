The code repository for team pOliver

Before running code install following modules(or make sure they are already installed):
cv2, asyncio, websockets, websocket, json, config, serial, math, argparse, os, time, numpy, datetime, threading, ast, pathlib, configparser, functools

motortest.py is used for giving motors speed individually
For our specific robot, values are 
first 3 bytes are PID to be given to robot
next 3 values are for motors, between 0 and 130 for motor speeds, 65 being 0 speed, 0 and 130 being -65 and 65 respectively
next *number* values are for thrower control, between 0 and 130 for thrower speeds, no shenanigans here
last value being a control byte for the mainboard

thresh.py is used for thresholding the image, different colour values of green, blue, magenta and black
same values are used later.

With the robot now working and colours thresholded, start multithread.py(!!change socket ip in the beginning of the file!!)
Send appropriate command via websocket to start/stop game logic. Basket colour can be changed when the logic section is running - can change basket mid round(good for testing purposes).
