#liikumise definitsioonid
import serial
import math
recv = 0
#muutsin ära kiiruse saatmise loogika - me saadame siia käskudele vahemiku -65 kuni 65, convertib meile õigeks
#rotate, ballrotate ja stop seda ei vaja
#aga ühtluse mõttes, sest omnitoball on *palju* lihtsam kui teeme nii


try:
    ser = serial.Serial('/dev/ttyACM1', 115200, timeout=1)
except:
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)


intFWS = 0
intFWF = 0
intRWS = 0
derFWS = 0
derFWF = 0
derRWS = 0
errFWS = 0
errFWF = 0
errRWS = 0
a_wheel_angle = 120
b_wheel_angle = 240
c_wheel_angle = 0
movement_direction_forward = 90

def returnRecv():
    return recv

def sendIt(values):
    global recv
    ser.write(bytearray(values))
    while ser.inWaiting():
        msg = (ser.read())
        try:
            recv = msg[len(msg) - 2]
        except:
            pass

def rotate(values, speed):
    values[3] = 65 + speed
    values[4] = 65 + speed
    values[5] = 65 + speed
    sendIt(values)

def reset(type):
    global intFWS, intFWF, intRWS, derFWS, derFWF, derRWS, errFWS, errFWF, errRWS

    if type == "FWS":
        intFWS = 0
        derFWS = 0
        errFWS = 0
    if type == "FWF":
        intFWF = 0
        derFWF = 0
        errFWF = 0
    if type == "RWS":
        intRWS = 0
        derRWS = 0
        errRWS = 0

def ballRotate(values, rearWheelSpeed, frontSideMovementSpeed, frontForwardSpeed):
    values[3] = int(round(65 - frontSideMovementSpeed + (frontForwardSpeed * -1), 0))
    values[4] = int(round(65 - frontSideMovementSpeed + frontForwardSpeed, 0))
    values[5] = int(65 + round(rearWheelSpeed, 0))#demokraatia
    #print(values)
    sendIt(values)


def pid2(sisend, integral, derivative, err_prev):
    P = 0.15
    I = 0.00007
    D = 0
    # sisend on error keskkohast
    error = 424 - sisend
    integral += error
    derivative = error - err_prev
    err_prev = error
    pööramiskiirus = P * error + integral * I + derivative * D

    return 640 - pööramiskiirus


def pidFrontWheelsSide(sisend):
    global intFWS
    global derFWS
    global errFWS
    P = 0.025
    I = 0.00004
    D = 0.006
    # integral = intFWS
    # print(sisend, err_prev)
    # sisend on error keskkohast
    error = 424 - sisend
    intFWS += error * 0.1
    derFWS = error - errFWS
    errFWS = error
    pööramiskiirus = P * error + intFWS * I + derFWS * D
    # print(int(pööramiskiirus))
    #print("Palli kesk:", sisend, (0 - pööramiskiirus), intFWS * I)
    return (0 - pööramiskiirus)
    #return 0

def pidFrontWheelsforward(sisend):
    global intFWF, derFWF, errFWF
    P = 0.015
    I = 0.0000
    D = 0.035
    if sisend < 200:
        #print("türannosaurus")
        return -45
    # sisend on error keskkohast
    error = 424 - sisend
    intFWF += error
    derFWF = error - errFWF
    errFWF = error
    pööramiskiirus = (P * error + intFWF * I + derFWS * D)
    #print("Pall edasi:", sisend, (0 - pööramiskiirus), intFWF * I)
    return (0 - pööramiskiirus)

def pidRearWheelSpeed(sisend, errors_array):
    # korvi keskel hoidmine
    global intRWS, derRWS, errRWS
    if sisend is None or sisend == 0:
        reset("RWS")
        return 45
    else:
        P = 0.025
        I = 0.000006
        D = 0.00
        # sisend on error keskkohast
        error = 455 - sisend
        errors_array.append(error)
        errors_array.pop(0)

        intRWS += error
        derRWS = error - errRWS
        errRWS = error
        pööramiskiirus = P * error + intRWS * I + derRWS * D
        #print("Korvi kesk:", sisend, (0 - pööramiskiirus), intRWS * I)
        return ((0 - pööramiskiirus))

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
    values[5] = 65 + calculate_linear_velocity(speed, c_wheel_angle, movement_direction_forward,
                                               mid_x, ball_X, ball_Y)
    values[4] = 65 + calculate_linear_velocity(speed, b_wheel_angle, movement_direction_forward,
                                               mid_x, ball_X, ball_Y)
    #print(values)
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


