import Config
import Protocol
import os
from socket import *
import threading

class Server:

    def __init__(self):
        self.conf=Config.Config(Config.Config.serverConfig)

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

        socket.send(Protocol.prepareMessage(Protocol.HEAD_READY, ""))

        with open(uploadFileName, "wb") as f:
            while True:
                data = socket.recv(1024)

                if not data:
                    break
                f.write(data)
            print(uploadFileName+" has been downloaded!")
            socket.close()


    # The main logic of the server
    def start(self, serverSocket, addr):
        print("Client connected: ",addr)
        try:

            while True:
                dataRec = serverSocket.recv(1024)
                header, msg = Protocol.decodeMessage(dataRec.decode())
                print("Header: ",header)
                print("Message: ", msg)

                if (header == Protocol.HEAD_REQUEST):
                    self.sendFileList(serverSocket)
                    break
                elif (header == Protocol.HEAD_FILE):
                    self.sendFile(serverSocket, self.conf.serverSharePath+"/"+msg)
                    break
                elif (header == Protocol.HEAD_UPLOAD):
                    self.receiveFile(serverSocket, self.conf.serverDownloadPath+"/"+msg)
                    break
                else:
                    serverSocket.send(Protocol.prepareMessage(Protocol.HEAD_ERROR, ""))
                    break
        except Exception as e:
            print("Error: ", e)

        print("Client disconnected: ", addr)
        serverSocket.close()
        


    def listenForClients(self):
        serverSocket = socket(AF_INET, SOCK_STREAM) # (ipv4, stream)

        serverSocket.bind(('', self.conf.serverPort))

        serverSocket.listen(12) # 12 clients

        print("Server is ready!")
        while True:
            connectionSocket, addr = serverSocket.accept()
            threading.Thread(target=self.start, args=[connectionSocket, addr]).start()


def main():
    s = Server()
    s.listenForClients()


if __name__ == "__main__":
    main()