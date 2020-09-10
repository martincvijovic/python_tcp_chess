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

# GAME STRING MATRIX
ROOK_WHITE = "RW"
KNIGHT_WHITE = "KW"
BISHOP_WHITE = "BW"
KING_WHITE = "KW"
QUEEN_WHITE = "QW"
PAWN_WHITE = "PW"
ROOK_BLACK = "RB"
KNIGHT_BLACK = "KB"
BISHOP_BLACK = "BB"
KING_BLACK = "KB"
QUEEN_BLACK = "QB"
PAWN_BLACK = "PB"
EMPTY_PIECE = "EMPTY"

# a method for safe communication (try/catch)
def safeSend(recvSocket_, msg_):
    try:
        recvSocket_.send(bytes(msg_.encode("utf-8")))
        return True
    except:
        return False

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
screen =  pygame.display.set_mode((500, 400))

pygame.display.set_caption("Chess")

# images for pygame
boardImage = pygame.image.load('board_new.png') 
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

# an empty image for the image matrix
nullImage = pygame.image.load('null.png')

pygame.display.set_icon(kingBlackImage) # game window icon

if myColor == COLOR_WHITE:
    myMove = True

initX = 0
initY = 0
delta = 50

# creating the game matrix (matrix of piece images)
# and movable matrix (flags for pieces the user can move)

gameMatrix = [[nullImage] * 8,[nullImage] * 8] # TODO : flip the game matrix horizontally for the black player

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



movableMatrix = [[0] * 8,[0] * 8] # 1 - the piece can be moved by user,
                                  # 0 - the piece cannot be moved by user
    
tempArray = [1] * 8

if myColor == COLOR_WHITE:
    for i in range(2):
        movableMatrix[i] = tempArray 
else:
    for i in range(6, 8):
        movableMatrix[i] = tempArray


while running == True:
    screen.fill((125,74,74))
    screen.blit(boardImage,(0, 0))    

    for i in range(0, 8):
        for j in range(0, 8):
            screen.blit(gameMatrix[j][i], (initX + i*delta, initY + j*delta)) 

    pygame.display.update()

    # TODO : add a server listener and update the matrices continuously

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            dummyVar = safeSend(s, END_GAME)
            s.close()
        
        if event.type == pygame.BUTTON_LEFT:
            if myMove == True:
                # TODO : check if the user can move the clicked piece, if so calculate the allowed fields (care for check), wait for action and update



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
