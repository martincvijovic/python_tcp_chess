import socket
import time
from random import randint, choice

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
        clientSockets[players].send(bytes(COLOR_WHITE, "utf-8"))
    else:
        print("Assigning color: BLACK")
        clientSockets[players].send(bytes(COLOR_BLACK, "utf-8"))

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

while msg != END_GAME:
    msg = s.recv(BUFFER_SIZE) # not working?
    if msg[0] == "0":
        clientSockets[1].send(bytes(msg, "utf-8"))
    else:
        clientSockets[0].send(bytes(msg, "utf-8"))
