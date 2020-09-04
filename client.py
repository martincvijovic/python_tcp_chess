import socket

# GIT TEST

PORT = 1998
BUFFER_SIZE = 4
SERVER_IP = socket.gethostname() # TODO : use a public (preferably static) IP for the server

# server message constants
COLOR_WHITE = "WWWW"
COLOR_BLACK = "BBBB"
GAME_READY = "RDY!"

# creating the client socket
# TODO : try catch
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_IP, PORT))

while True: # TODO : Thread it
    msg = s.recv(BUFFER_SIZE) 
    print(msg.decode("utf-8"))