from socket import *

serverName="localhost"
serverPort=12000

clientSocket=socket(AF_INET, SOCK_DGRAM)

message=input("Enter a message to be converted to upper case: ")

clientSocket.sendto(message.encode(), (serverName, serverPort))

modifiedMessage,serverAddress=clientSocket.recvfrom(2048)
print(modifiedMessage.decode())

clientSocket.close()