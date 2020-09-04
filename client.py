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

msg = ""
myColor = ""

while msg != GAME_READY: # TODO : Thread it
    msg = s.recv(BUFFER_SIZE) 
    myColor = msg.decode("utf-8")

print("Game ready, color: " + myColor)
    