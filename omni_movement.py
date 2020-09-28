import cv2
import serial
from math import cos, sqrt, atan2, floor

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



def omniDrive(robotSpeedX, robotSpeedY):
    # Calculating speed
    robotSpeed = sqrt(robotSpeedX * robotSpeedX + robotSpeedY * robotSpeedY)  # m/s
    # Calculating direction angle
    robotDirectionAngle = atan2(robotSpeedY, robotSpeedX)  # rad
    omni_move(robotSpeed, robotDirectionAngle)


def omni_move(robotSpeed, robotDirectionAngle):
    # Wheel speed calculation
    wheelLinearVelocity0 = robotSpeed * cos(robotDirectionAngle - wheelAngel0)
    wheelLinearVelocity1 = robotSpeed * cos(robotDirectionAngle - wheelAngel1)
    wheelLinearVelocity2 = robotSpeed * cos(robotDirectionAngle - wheelAngel2)

    wheelSpeedToMainboardUnits = gearboxReductionRatio * encoderEdgesPerMotorRevolution / \
                                 (2 * wheelRadius * pidControlFrequency)

    wheelAngularSpeedMainboardUnits0 = floor(wheelLinearVelocity0 * wheelSpeedToMainboardUnits)
    wheelAngularSpeedMainboardUnits1 = floor(wheelLinearVelocity1 * wheelSpeedToMainboardUnits)
    wheelAngularSpeedMainboardUnits2 = floor(wheelLinearVelocity2 * wheelSpeedToMainboardUnits)

    move = 'sd' + str(wheelAngularSpeedMainboardUnits0) + ':' + \
           str(wheelAngularSpeedMainboardUnits1) + ':' + str(wheelAngularSpeedMainboardUnits2)

    print(move)
    ser.write(move.encode())
    print("sent")
    while ser.inWaiting():
        print(ser.read())


ser.close()
