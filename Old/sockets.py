from socket import *

serverName="localhost" # or IP address
serverPort=12000 # ports range from 0-65536 (2^16), first 1024 reserved for highly used applications

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', serverPort)) # '' defaults to localhost

print("The sever is ready to receive")

while True:
    message,clientAddress = serverSocket.recvfrom(2048) # 2048 bytes is buffer size

    modifiedMessage=message.decode().upper() # convert to uppercase ascii
    serverSocket.sendto(modifiedMessage.encode(), clientAddress) #send modified message back to client