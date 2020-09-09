import socket
import threading
import pygame

PORT = 1998
BUFFER_SIZE = 5
SERVER_IP = socket.gethostname() # TODO : use a public (preferably static) IP for the server

# desi bubo
# evo me bubo

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
screen =  pygame.display.set_mode((870, 870))

boardImage = pygame.image.load('board.png') # background
rookWhiteImage = pygame.image.load('rook_white.png')
knightWhiteImage = pygame.image.load('knight_white.png')
bishopWhiteImage = pygame.image.load('bishop_white.png')
queenWhiteImage = pygame.image.load('queen_white.png')
kingWhiteImage = pygame.image.load('king_white.png')
pawnWhiteImage = pygame.image.load('pawn_white.png')

rookBlackImage = pygame.image.load('rook_black.png')
knightBlackImage = pygame.image.load('knight_black.png')
bishopBlackImage = pygame.image.load('bishop_black.png')
queenBlackImage = pygame.image.load('queen_black.png')
kingBlackImage = pygame.image.load('king_black.png')
pawnBlackImage = pygame.image.load('pawn_black.png')

nullImage = pygame.image.load('null.png')

if myColor == COLOR_WHITE:
    myMove = True
    # print("I am white, i ping first.")

# start the server listener:

# initX = 5
# initY = 5
# delta = 58

initX = 0 # initial coordinates 
initY = 0 
delta = 102 # number of steps to move to the next field

while running == True:
    screen.fill((125,74,74))
    screen.blit(boardImage,(0, 0))

    # add all the initial pieces
    # TODO : 3 arrays, x[i], y[i], piece[i]
    # test purposes:

    # initial image matrix (TODO : flip horizontal for black player)
    # possible values: image var names, null for nothing

    gameMatrix = [[nullImage] * 8,[nullImage] * 8]

    for i in range(8):
        for j in range(8):
            gameMatrix.append(nullImage)


    for i in range(8):
        gameRow = [nullImage] * 8
        for j in range(8):
            if i == 1:
                gameRow[j] = pawnBlackImage
            if i == 6:
                gameRow[j] = pawnWhiteImage  
            if i == 0:
                if j == 0 or j == 7:
                    gameRow[j] = rookBlackImage
                if j == 1 or j == 6:
                    gameRow[j] = knightBlackImage
                if j == 2 or j == 5:
                    gameRow[j] = bishopBlackImage
                if j == 3:
                    gameRow[j] = queenBlackImage
                if j == 4:
                    gameRow[j] = kingBlackImage
            if i == 7:
                if j == 0 or j == 7:
                    gameRow[j] = rookWhiteImage
                if j == 1 or j == 6:
                    gameRow[j] = knightWhiteImage
                if j == 2 or j == 5:
                    gameRow[j] = bishopWhiteImage
                if j == 3:
                    gameRow[j] = queenWhiteImage
                if j == 4:
                    gameRow[j] = kingWhiteImage
        gameMatrix[i] = gameRow

    for i in range(0, 8):
        for j in range(0, 8):
            screen.blit(gameMatrix[j][i], (initX + i*delta, initY + j*delta)) 
            

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
