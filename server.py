import socket
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

# creating the server socket on localhost
# TODO : try/catch
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), PORT))
s.listen(2) # two players

print("Server listening on port " + str(PORT))

# accept 2 players, assign color, notify when game ready

players = 0 # currently connected players
playerColor = str(randint(0, 1)) # randomly assigning white/black pieces to player 1

clientSockets = []
clientIPs = []

while players < 2:
    clientSockets[players], clientIPs[players] = s.accept()
    players = players + 1

    print("Incoming socket from " + str(clientIP))
    if playerColor = INT_WHITE:
        clientSocket.send(bytes(COLOR_WHITE, "utf-8"))
    else:
        clientSocket.send(bytes(COLOR_BLACK, "utf-8"))

    playerColor = 1 - playerColor # changing the pieces color for the second player

# both players connected, start the game
for i in range(0, 1):
    clientSockets[i].send(bytes(GAME_RDY))

# the game:
while True:
    # TODO : just accept and forward messages

