import Config
import Protocol
import os
from socket import *

class Server:

    def __init__(self):
        self.conf=Config.Config()

    def getFileList(self):
        return os.listdir(self.conf.serverSharePath)

    def sendFileList(self, serverSocket):
        message = Protocol.prepareFileList(Protocol.HEAD_REQUEST, self.getFileList())
        serverSocket.send(message)

    def sendFile(self, serverSocket, fileName):
        f=open(fileName, 'rb')
        l=f.read(1024)
        while(l):
            serverSocket.send(l)
            l=f.read(1024)




    def receiveFile(self, socket, uploadFileName):
        with open(uploadFileName, "wb") as f:
            while True:
                data = socket.recv(1024)
                if not data:
                    break
                f.write(data)
            print(uploadFileName+" has been downloaded!")
            socket.close()


    # The main logic of the server
    def start(self):
        
        serverSocket = socket(AF_INET, SOCK_STREAM) # (ipv4, stream)

        serverSocket.bind(('', self.conf.serverPort))

        serverSocket.listen(1) # 1 client

        print("Server is ready!")

        while True:
            connectionSocket, addr = serverSocket.accept()
            dataRec = connectionSocket.recv(1024)
            header, msg = Protocol.decodeMessage(dataRec.decode())

            if (header == Protocol.HEAD_REQUEST):
                self.sendFileList(connectionSocket)
            elif (header == Protocol.HEAD_FILE):
                self.sendFile(connectionSocket, self.conf.serverSharePath+"/"+msg)
            elif (header == Protocol.HEAD_UPLOAD):
                self.receiveFile(connectionSocket, self.conf.serverDownloadPath+"/"+msg)
            else:
                connectionSocket.send(Protocol.prepareMessage(Protocol.HEAD_ERROR, ""))
            connectionSocket.close()


def main():
    s = Server()
    s.start()


if __name__ == "__main__":
    main()