import cv2
import serial
from math import cos, sqrt, atan2, floor, radians
values = [25, 25, 0, 70, 70, 70, 0, 170]
# esimene vasak 0
# tagumine 1
# esimene parem 2
# Serial setup

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

# Variables:
robotSpeedX = 2  # m/s
robotSpeedY = 2  # m/s
wheelAngel0 = 0  # rad
wheelAngel1 = 120  # rad
wheelAngel2 = 240  # rad

gearboxReductionRatio = 1 / 19
encoderEdgesPerMotorRevolution = 64
wheelRadius = 0.0038  # m
pidControlFrequency = 60  # Hz

def write(move):
    #print(move)
    ser.write(bytearray(move))
    #print("sent")
    while ser.inWaiting():
        (ser.read())

def stop():
    values[3] = 65
    values[4] = 65
    values[5] = 65
    write(values)

def turnLeft():
    values[3] = 63
    values[4] = 63
    values[5] = 63
    write(values)

def turnRight():
    values[3] = 67
    values[4] = 67
    values[5] = 67
    write(values)

def turnFast():
    values[3] = 70
    values[4] = 70
    values[5] = 70
    write(values)

def forward():
    values[3] = 75
    values[4] = 55
    values[5] = 65
    write(values)

def omniDrive(robotSpeedX, robotSpeedY):
    # Calculating speed
    robotSpeed = sqrt(robotSpeedX * robotSpeedX + robotSpeedY * robotSpeedY)  # m/s
    # Calculating direction angle
    robotDirectionAngle = atan2(robotSpeedY, robotSpeedX)  # rad
    omni_move(robotSpeed, robotDirectionAngle)


def omni_move(robotSpeed, robotDirectionAngle):
    # Wheel speed calculation
    wheelLinearVelocity0 = robotSpeed * cos(radians(robotDirectionAngle - wheelAngel0))
    wheelLinearVelocity1 = robotSpeed * cos(radians(robotDirectionAngle - wheelAngel1))
    wheelLinearVelocity2 = robotSpeed * cos(radians(robotDirectionAngle - wheelAngel2))

    wheelSpeedToMainboardUnits = gearboxReductionRatio * encoderEdgesPerMotorRevolution / \
                                 (2 * wheelRadius * pidControlFrequency)

    wheelAngularSpeedMainboardUnits0 = floor(wheelLinearVelocity0 * wheelSpeedToMainboardUnits)
    wheelAngularSpeedMainboardUnits1 = floor(wheelLinearVelocity1 * wheelSpeedToMainboardUnits)
    wheelAngularSpeedMainboardUnits2 = floor(wheelLinearVelocity2 * wheelSpeedToMainboardUnits)

    # move = 'sd:' + str(wheelAngularSpeedMainboardUnits0) + ':' + \
    #       str(wheelAngularSpeedMainboardUnits1) + ':' + str(wheelAngularSpeedMainboardUnits2) + ' \n'
    move = 'sd:' + str(int(wheelLinearVelocity0)) + ':' + \
           str(int(wheelLinearVelocity1)) + ':' + str(int(wheelLinearVelocity2)) + ' \n'
    move = values
    #[25, 25, 0, 70, 70, 70, 0, 170]
    move[3] = int(wheelLinearVelocity0)
    move[4] = int(wheelLinearVelocity1)
    move[5] = int(wheelLinearVelocity2)

    write(move)

