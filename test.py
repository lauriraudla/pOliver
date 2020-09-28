# pip3 install pynput on käsk

import serial
import time
from pynput.keyboard import Key, Listener

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

firstMillis = int(round(time.time() * 1000))


def on_press(key):
    print('{0} pressed'.format(
        key))
    if key == Key.up:
        return ser.write(b'sd:-40:0:40:0\n')
    if key == Key.down:
        return ser.write(b'sd:40:0:-40:0\n')
    if key == Key.right:
        return ser.write(b'sd:15:15:15:0\n')
    if key == Key.left:
        return ser.write(b'sd:-15:-15:-15:0\n')


def on_release(key):
    print('{0} release'.format(
        key))
    if key == Key.esc:
        # Stop listener
        return False
    if key == Key.up:
        return ser.write(b'sd:0:0:0:0\n')
    if key == Key.down:
        return ser.write(b'sd:0:0:0:0\n')
    if key == Key.right:
        return ser.write(b'sd:0:0:0:0\n')
    if key == Key.left:
        return ser.write(b'sd:0:0:0:0\n')


# Collect events until released
with Listener() as listener:
    listener.join

# with Listener(
#         on_press=on_press,
#         on_release=on_release) as listener:
#     listener.join()