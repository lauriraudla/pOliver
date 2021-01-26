#liikumise definitsioonid
import serial
import math
#muutsin ära kiiruse saatmise loogika - me saadame siia käskudele vahemiku -65 kuni 65, convertib meile õigeks
#rotate, ballrotate ja stop seda ei vaja
#aga ühtluse mõttes, sest omnitoball on *palju* lihtsam kui teeme nii

try:
    ser = serial.Serial('/dev/ttyACM1', 115200, timeout=1)
except:
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

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

def ballRotate(values, speed, pit, forwardSpeed):
    values[3] = 65 - pit + (forwardSpeed * -1)
    values[4] = 65 - pit + forwardSpeed
    values[5] = 65 + speed
    print(values)
    sendIt(values)

def ballRotateExact(values, speed):
    values[3] = 64
    values[4] = 67
    values[5] = 65 + speed
    sendIt(values)

def stop(values):
    values[3] = 65
    values[4] = 65
    values[5] = 65
    sendIt(values)

def stopAll(values):
    values[3] = 65
    values[4] = 65
    values[5] = 65
    values[6] = 0
    sendIt(values)

def startThrow(values,speed):
    values[6] = speed
    sendIt(values)

def endThrow(values):
    values[6] = 0
    sendIt(values)

def forward(values,speed):
    values[3] = 65 + speed
    values[4] = 65 - speed
    values[5] = 65
    sendIt(values)

def Right(values):
    values[3] = 60
    values[4] = 60
    values[5] = 70
    sendIt(values)

def Left(values):
    values[3] = 70
    values[4] = 70
    values[5] = 60
    sendIt(values)

def toBall(values,speed,ball, middle=None):#kus ball on 2 elemendiline array: X ja Y
    if middle is None:
        mid_x = 640
    else:
        mid_x = middle
    ball_X = ball[0]
    ball_Y = ball[1]

    values[3] = 65 + calculate_linear_velocity(speed, a_wheel_angle, movement_direction_forward,
                                                        mid_x, ball_X, ball_Y)
    values[5] = 65 - calculate_linear_velocity(speed, c_wheel_angle, movement_direction_forward,
                                                       mid_x, ball_X, ball_Y)
    values[4] = 65 + calculate_linear_velocity(speed, b_wheel_angle, movement_direction_forward,
                                                        mid_x, ball_X, ball_Y)
    print(values)
    sendIt(values)

def calculate_linear_velocity(wheel_speed, wheel_angle, direction, mid_x=None, X=None, Y=None):
    if Y != None and Y != 0:
        direction = calculate_direction_angle(mid_x, X, Y, direction)
        wheel_linear_velocity = wheel_speed *  math.cos(math.radians(direction - wheel_angle))
    else:
        wheel_linear_velocity = wheel_speed *  math.cos(math.radians(direction - wheel_angle))

    return int(wheel_linear_velocity)

def calculate_direction_angle(mid_x, X, Y, direction):
    direction = int(math.degrees(math.atan((mid_x - X) / Y)) + direction)
    return direction


def pid(sisend, integral, derivative, err_prev):
    P = 0.012
    I = 0.015
    D = 0
    # sisend on error keskkohast
    error = 640 - sisend
    integral += error
    derivative = error - err_prev
    err_prev = error
    pööramiskiirus = P * error + integral * I + derivative * D

    return 640 - pööramiskiirus

def pid2(sisend, integral, derivative, err_prev):
    P = 0.01
    I = 0.04
    D = 0
    # sisend on error keskkohast
    error = 640 - sisend
    integral += error
    derivative = error - err_prev
    err_prev = error
    pööramiskiirus = P * error + integral * I + derivative * D

    return 640 - pööramiskiirus

def pidBallCenter(sisend, integral, derivative, err_prev):
    P = 0.02
    I = 0.015
    D = 0
    #print(sisend, err_prev)
    # sisend on error keskkohast
    error = 640 - sisend
    integral += error
    derivative = error - err_prev
    err_prev = error
    pööramiskiirus = P * error + integral * I + derivative * D
    #print(int(pööramiskiirus))

    return int(0 - pööramiskiirus)

def pidBallCenterForward(sisend, integral, derivative, err_prev):
    P = 0.02
    I = 0.015
    D = 0
    #print(sisend, err_prev)
    if sisend < 540:
        return -30
    #(1 - sisend/720)
    # sisend on error keskkohast
    error = 640 - sisend
    integral += error
    derivative = error - err_prev
    err_prev = error
    pööramiskiirus = P * error + integral * I + derivative * D
    #print(int(0-pööramiskiirus))

    return int(0 - pööramiskiirus)


def pidBallCenterRotateSpeed(sisend, integral, derivative, err_prev, errors_array):
    # korvi keskel hoidmine
    if sisend is None or sisend == 0:
        return 30
    else:
        P = 0.015
        I = 0.02
        D = 0
        #print(sisend, err_prev)
        # sisend on error keskkohast
        error = 610 - sisend
        errors_array.append(error)
        errors_array.pop(0)

        #print(errors_array)
        integral += error
        derivative = error - err_prev
        err_prev = error
        pööramiskiirus = P * error + integral * I + derivative * D
        #print(int(pööramiskiirus))
        return int((0 - pööramiskiirus))
        #return int(math.ceil(0 - pööramiskiirus))