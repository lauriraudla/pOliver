import serial
from math import cos, sqrt, atan2, floor, radians
values = [25, 0, 0, 70, 0, 0, 0, 170]

ser = serial.Serial('COM4', 115200, timeout=1)

def write(move):
    print(move)
    ser.write(bytearray(move))
    #print("sent")
    while ser.inWaiting():
        (ser.read())

while True:
    inp = input("sisesta:")
    if inp == "1":
        write(values)
    elif inp == "2":
        change = int(input("nr:"))
        if change == 0:
            data = int(input("väärtus:"))
            values[change] = data
        elif change == 1:
            data = int(input("väärtus:"))
            values[change] = data
        elif change == 2:
            data = int(input("väärtus:"))
            values[change] = data
        elif change == 3:
            data = int(input("väärtus:"))
            values[change] = data
        elif change == 4:
            data = int(input("väärtus:"))
            values[change] = data
        elif change == 5:
            data = int(input("väärtus:"))
            values[change] = data
        elif change == 6:
            data = int(input("väärtus:"))
            values[change] = data
        elif change == 7:
            data = int(input("väärtus:"))
            values[change] = data
    else:
        break