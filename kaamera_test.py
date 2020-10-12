import cv2
import pyrealsense2 as rs
import serial

cap = cv2.VideoCapture(2)

ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
test = 'sd:0:20:0 \n'
while True:
    _,frame = cap.read()
    cv2.imshow("frame", frame)
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow("gray", gray)
    ser.write(test.encode('ascii'))



    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
