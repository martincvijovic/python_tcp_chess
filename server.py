import socket

PORT = 1998 

# creating the server socket on localhost
# TODO : try/catch
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), PORT))
s.listen(2) # two players

print("Server listening on port " + str(PORT))

while True:
    clientSocket, clientIP = s.accept()
    print("Incoming socket from " + str(clientIP))
    clientSocket.send(bytes("TEST from server", "utf-8"))


