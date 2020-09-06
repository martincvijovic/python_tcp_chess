import socket
import threading
import pygame

PORT = 1998
BUFFER_SIZE = 5
SERVER_IP = socket.gethostname() # TODO : use a public (preferably static) IP for the server

# server message constants
COLOR_WHITE = "WWWW"
COLOR_BLACK = "BBBB"
GAME_READY = "RDY!"
END_GAME = "END"

print("Connecting to the server...")

# creating the client socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((SERVER_IP, PORT))

print("Connected. Waiting for the opponent...")

msg = ""
myColor = ""

msgCnt = 1

while (msg != GAME_READY): # 2 messages will be received : COLOR, ID
    msg = s.recv(BUFFER_SIZE) 
    if (msgCnt == 1):
        myColor = msg.decode("utf-8")
    if (msgCnt == 2):
        myID = msg.decode("utf-8")
        break
    msgCnt = msgCnt + 1

print("Game ready, color: " + myColor + ", ID: " + myID)

myMove = False
running = True


# pygame window settings
pygame.display.set_caption("Chess by Martin Cvijovic")
pygame.init()
screen =  pygame.display.set_mode((600, 500))

boardImage = pygame.image.load('board.png') # background
rookWhiteImage = pygame.image.load('rook_white.png')

if myColor == COLOR_WHITE:
    myMove = True
    # print("I am white, i ping first.")

# start the server listener:

initX = 5 # initial coordinates 
initY = 5 
delta = 58 # number of steps to move to the next field

while running == True:
    screen.fill((125,74,74))
    screen.blit(boardImage,(0, 0))

    # add all the initial pieces
    # TODO : 3 arrays, x[i], y[i], piece[i]
    # test purposes:
    for i in range(0, 8):
        for j in range(0, 2):
            screen.blit(rookWhiteImage, (initX + i*delta, initY + j*delta)) 

    for i in range(0, 8):
        for j in range(6, 8):
            screen.blit(rookWhiteImage, (initX + i*delta, initY + j*delta))

    pygame.display.update()
    for event in pygame.event.get():
        # actions happen here
        if event.type == pygame.QUIT:
            running = False
            s.close()


'''
while running == True:
    while myMove == False:
        msg = s.recv(BUFFER_SIZE)
        myMove = True
        print("Received a ping from the opponent")
        print(msg.decode("utf-8"))
    print("Trying to ping the opponent...")
    s.send(bytes("PING".encode("utf-8")))
    myMove = False
'''