import socket
import time
from random import randint, choice
import threading
    

# buffer size is equal to message size (4 chars will do)
BUFFER_SIZE = 4
PORT = 1998 
# colors
COLOR_WHITE = "WWWW"
COLOR_BLACK = "BBBB"
INT_WHITE = 0 # binding random generated 0/1 to colors
INT_BLACK = 1   
# server specific messages and constants
GAME_READY = "RDY!"
PLAYER_CNT = 2
END_GAME = "END"

# creating the server socket on localhost
# TODO : try/catch

connectionSuccess = False

print("Trying to bind on port " + str(PORT) + "...")

while (connectionSuccess == False):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), PORT))
        s.listen(2) # two players
        connectionSuccess = True
    except OSError:
        print("Port " + str(PORT) + " in use, retrying after 5 seconds...")
        connectionSuccess = False
        time.sleep(5)

print("Server listening on port " + str(PORT))

# accept 2 players, assign color, notify when game ready

players = 0 # currently connected players
playerColor = randint(0, 1) # randomly assigning white/black pieces to player 1

clientSockets = []
clientIPs = []

while players < 2:
    socket_, ip_ = s.accept()

    clientSockets.append(socket_)
    clientIPs.append(ip_)

    print("Incoming connection from " + str(clientIPs[players]))

    if playerColor == INT_WHITE:
        print("Assigning color: WHITE")
        clientSockets[players].send(bytes(COLOR_WHITE.encode("utf-8")))
    else:
        print("Assigning color: BLACK")
        clientSockets[players].send(bytes(COLOR_BLACK.encode("utf-8")))

    playerColor = 1 - playerColor # changing the pieces color for the second player

    players = players + 1

# both players connected, start the game
print("Both players connected, starting the game...")
i = 0
for client in clientSockets:
    client.send(bytes(str(i), "utf-8")) # identificating the clients
    i = i + 1


# game messages format : PXYxy
# P - player count (1 or 2)
# X, Y - piece coordinates
# x, y - piece new coordinates (rule check done on client side)
# server just forwards the messages

msg = ""

def firstListener():
    while True: # TODO : create an end game condition
        msg1=clientSockets[0].recv(BUFFER_SIZE)
        if len(msg1) > 0:    
            msg = msg1.decode("utf-8")
            print("Incoming message from P0 to P1: " + msg)
            clientSockets[1].send(bytes("PING".encode("utf-8")))     

def secondListener():
    while True: # TODO : create an end game condition
        msg2=clientSockets[1].recv(BUFFER_SIZE)
        if len(msg2) > 0:
            msg = msg2.decode("utf-8")
            print("Incoming message from P1 to P0: " + msg)
            clientSockets[0].send(bytes("PONG".encode("utf-8"))) 


thread1 = threading.Thread(target=firstListener)
thread2 = threading.Thread(target=secondListener)

thread1.start()
thread2.start()