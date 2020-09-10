import socket
import time
from random import randint, choice
import threading
    
# buffer size = message size 
BUFFER_SIZE = 4
PORT = 1998 

# server-specific messages and constants
COLOR_WHITE = "WWWW"
COLOR_BLACK = "BBBB"

INT_WHITE = 0 # IDs
INT_BLACK = 1   

GAME_READY = "RDY!"
PLAYER_CNT = 2
END_GAME = "END" 


def safeSend(recvSocket_, msg_):
    try:
        recvSocket_.send(bytes(msg_.encode("utf-8")))
        return True
    except:
        return False

def socketListener(ID_, clientSockets_):
    connected = True

    while connected:
        msg = clientSockets_[1-ID_].recv(BUFFER_SIZE)

        if len(msg) > 0:
            msg = msg.decode("utf-8")

            if msg == END_GAME:
                connected = False

            print("Incoming message from P" + ID_ + " to P" + 1 - ID_)
            connected = safeSend(clientSockets_[1 - ID_], msg)

def newGame():

    print("NEW GAME!")

    players = 0 
    playerColor = randint(0, 1) 

    clientSockets = []
    clientIPs = []

    thread1 = threading.Thread(target=socketListener, args=(0, clientSockets))
    thread2 = threading.Thread(target=socketListener, args=(1, clientSockets))

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

    print("Both players connected, starting the game...")
    i = 0
    for client in clientSockets:
        client.send(bytes(str(i), "utf-8")) # identifying clients
        i = i + 1

    # game messages format : PXYxy
    # P - player ID (1 or 2)
    # X, Y - old piece coordinates
    # x, y - new piece coordinates (chess rule check done on client side)
    # server just forwards the messages

    thread1.start()
    thread2.start()
    
    # if any of the players disconnect, disconnect all the clients and start a new game

    thread1.join()
    thread2.join()
    
    for client in clientSockets:
        client.close()
    
    newGame()


# main program
# creating the server socket on localhost

#new

connectionSuccess = False

print("Trying to bind on port " + str(PORT) + "...")

while (connectionSuccess == False):
    try:
        
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((socket.gethostname(), PORT))
        s.listen(2) # max. of 2 possible players
        connectionSuccess = True
    except OSError:
        print("Port " + str(PORT) + " in use, retrying after 5 seconds...")
        connectionSuccess = False
        time.sleep(5)

print("Server listening on port " + str(PORT))

newGame()
