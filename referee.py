import socket
import sys
from _thread import *  # low level threading library
import json

robot = "pOliver"
go = False
basket = "color"
signal = "signal"



HOST = ''  # symbolic name meaning all available interfaces
PORT = 8887  # arbitrary non-privileged port
numconn = 10  # number of simultaneous connections
buffer_size = 4096  # input buffer size

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('...socket created...')

# bind socket to local host and port
try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('...bind failed...error code: ' + str(msg.arg[0]) + ', error message: ' + msg.arg[1])
    sys.exit()

print('...socket bind complete...')

# make socket to listen incoming connections
s.listen(numconn)
print('...socket now listening...')


# function for handling connections...this will be used to create threads
def clientthread(conn):
    global go, basket, signal
    # sending message to connected client
    conn.send('pOliver connected \n'.encode())  # send only takes bytes
    # infinite loop so that the function does not terminate and the thread does not end
    while True:
        try:
            # receiving from client

            data = conn.recv(buffer_size)  # receives bytes
            andmed = data.decodereferee.py
            commands = json.loads(str(andmed))
            print(commands)
            signal = commands["signal"]
            robot_index = commands["targets"].index(robot)
            basket = commands["baskets"][robot_index]
            print(basket)
            if not data:
                break
            reply = 'pOliver...ACK...' + signal  # decode bytes to string
            conn.sendall(reply.encode())
        except socket.error as message:  # error, for example if the connection is closed
            print(message)
            break
    # came out of loop
    conn.close()


# now keep talking with the client (infinite loop)
while True:
    # wait to accept a connection - blocking call
    conn, addr = s.accept()

    # display client information
    print('...connected with ' + addr[0] + ':' + str(addr[1]))

    # start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function
    start_new_thread(clientthread, (conn,))

s.close()


