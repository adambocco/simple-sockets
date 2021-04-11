from socket import *

serverName="localhost"
serverPort=12001

clientSocket = socket(AF_INET, SOCK_STREAM) # SOCK_STREAM means this is a TCP connection

clientSocket.connect((serverName, serverPort))

message=input("Enter a lowercase sentence: ")
clientSocket.send(message.encode()) # dont need 'sendto()' because TCP connection already established above

modifiedMessage= clientSocket.recv(2048) # dont need recvfrom() because conn. established already

print(modifiedMessage.decode())

clientSocket.close()