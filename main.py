import cv2
import vision_test
import time
import serial, keyboard



image_thread = vision_test.imageCapRS2()

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)

while True:
    test_string = 'sd:10:0:-10 \n'
    #ser.write(test_string.encode())
    #reading = ser.readline()
    #print(reading)
    frame = image_thread.getFrame()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    cv2.imshow("frame",frame)
    k = cv2.waitKey(1)
    if k == ord("q"):
        image_thread.setStopped(False)
        break
    a = str(input())
    if a != '':
        try:
            if a == 'w':
                print("pressed W")
                ser.write(test_string.encode())
        except:
            break

cv2.destroyAllWindows()
