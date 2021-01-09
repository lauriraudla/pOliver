#liikumise definitsioonid
import serial
import math
#muutsin ära kiiruse saatmise loogika - me saadame siia käskudele vahemiku -65 kuni 65, convertib meile õigeks
#rotate, ballrotate ja stop seda ei vaja
#aga ühtluse mõttes, sest omnitoball on *palju* lihtsam kui teeme nii

ser = serial.Serial('/dev/ttyACM1', 115200, timeout=1)

a_wheel_angle = 120
b_wheel_angle = 240
c_wheel_angle = 0
movement_direction_forward = 90

def sendIt(values):
    ser.write(bytearray(values))
    while ser.inWaiting():
        (ser.read())

def rotate(values, speed):
    values[3] = 65 + speed
    values[4] = 65 + speed
    values[5] = 65 + speed
    sendIt(values)

def ballRotate(values, speed):
    values[3] = 63
    values[4] = 67
    values[5] = 65 + speed
    sendIt(values)

def stop(values):
    values[3] = 65
    values[4] = 65
    values[5] = 65
    sendIt(values)

def startThrow(values,speed):
    values[6] = speed
    sendIt(values)

def endThrow(values):
    values[6] = 0
    sendIt(values)

def forward(values):
    values[3] = 85
    values[4] = 45
    values[5] = 65
    sendIt(values)

def toBall(values,speed,ball):#kus ball on 2 elemendiline array: X ja Y
    mid_x = 640
    ball_X = ball[0]
    ball_Y = ball[1]

    values[3] = 65 + calculate_linear_velocity(speed, a_wheel_angle, movement_direction_forward,
                                                        mid_x, ball_X, ball_Y)
    values[5] = 65 - calculate_linear_velocity(speed, b_wheel_angle, movement_direction_forward,
                                                       mid_x, ball_X, ball_Y)
    values[4] = 65 + calculate_linear_velocity(speed, c_wheel_angle, movement_direction_forward,
                                                        mid_x, ball_X, ball_Y)
    print(values)
    sendIt(values)

def calculate_linear_velocity(wheel_speed, wheel_angle, direction, mid_x=None, X=None, Y=None):
    if Y != None and Y != 0:
        direction = calculate_direction_angle(mid_x, X, Y, direction)
        wheel_linear_velocity = wheel_speed * math.cos(math.radians(direction - wheel_angle))
    else:
        wheel_linear_velocity = wheel_speed * math.cos(math.radians(direction - wheel_angle))

    return int(wheel_linear_velocity)

def calculate_direction_angle(mid_x, X, Y, direction):
    direction = int(math.degrees(math.atan((mid_x - X) / Y)) + direction)
    return direction

