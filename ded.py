p = '0000000000000000'
i = '0000000000000000'
d = '0000000000000000'

speed1 = '0000000000000000'
speed2 = '0000000000000000'
speed3 = '0000000000000000'
thrower = '0000000000000000'

de = '10101010101010'

int_to_bin = bin(6)[2:].zfill(16)

big_chungus = p+i+d+speed1+speed2+speed3+thrower+de
print(big_chungus)

import serial
from math import cos, sqrt, atan2, floor, radians


#ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

def write(move):
    print(move)
    print(move.encode('ascii'))
    #print("sent")
    #while ser.inWaiting():
    #    (ser.read())

while True:
    inp = input("sisesta:")
    if inp == "1":
        write(big_chungus)
    elif inp == "2":
        data = input("kiirus:")
        speed1 = int_to_bin = bin(int(data))[2:].zfill(16)
        big_chungus = p+i+d+speed1+speed2+speed3+thrower+de
    else:
        break
