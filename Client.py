import Protocol
import Config
import os
from socket import *


class Client:
    
    def __init__(self):
        self.conf = Config.Config(Config.Config.clientConfig)

    # Function to print out user menu

    def printMenu(self):
        print("Welcome to Simple File Sharing System!")
        print("Please select an operation from the menu: ")
        print("=========================================")
        print("1. View the List of Available Files")
        print("2. Download File")
        print("3. Upload File")
        print("4. Quit")
        print("=========================================")
    
    # Function to get user selection from the menu

    def getUserSelection(self):
        selection = 0

        while selection > 4 or selection < 1:
            self.printMenu()
            try:
                selection = int(input())
            except:
                selection=0
            if (selection <=4 and selection >=1):
                return selection
            print("Invalid Option")

    # Build connection to the server

    def connect(self):
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((self.conf.serverName, self.conf.serverPort))
        return clientSocket

    # Function to get file list from the server
    
    def getDownloadFileList(self):
        mySocket=self.connect()
        
        request = Protocol.prepareMessage(Protocol.HEAD_REQUEST, "")
        mySocket.send(request)

        header, msg = Protocol.decodeMessage(mySocket.recv(1024).decode())

        mySocket.close()

        if (header == Protocol.HEAD_REQUEST):
            files = msg.split(",")
            self.downloadFileList = []
            for f in files:
                self.downloadFileList.append(f)


    def getUploadDownloadFileList(self):
        self.uploadDownloadFileList = os.listdir(self.conf.clientSharePath)

    def printUploadDownloadFileList(self):
        for i,f in enumerate(self.uploadDownloadFileList):
            print('{:<3d}{}'.format(i, f))


    # Function to print out file names

    def printDownloadFileList(self):
        for i,f in enumerate(self.downloadFileList):
            print('{:<3d}{}'.format(i, f))


    # Function to let user to select a file from the list

    def selectDownloadFile(self):
        try:
            if (len(self.downloadFileList) == 0):
                self.getDownloadFileList()
        except: 
            self.getDownloadFileList()
        ans = -1
        while (ans < 0 or ans >= len(self.downloadFileList)):
            self.printDownloadFileList()
            print("Please select the file you want to download (Enter the number of the file)")
            try:
                ans = int(input())
            except:
                ans = -1
            if (ans >= 0 and ans < len(self.downloadFileList)):
                return self.downloadFileList[ans]
            print("Invalid number")


    def selectUploadFile(self):

        self.getUploadDownloadFileList()
        ans = -1
        while (ans < 0 or ans > len(self.uploadDownloadFileList)):
            self.printUploadDownloadFileList()
            print("Please select the file you want to upload (Enter the number of the file)")
            try:
                ans = int(input())
            except:
                ans = -1
            if (ans >= 0 and ans < len(self.uploadDownloadFileList)):
                return self.uploadDownloadFileList[ans]
            print("Invalid number")


    # Function to download file

    def downloadFile(self, downloadFileName):
        mySocket = self.connect()
        request = Protocol.prepareMessage(Protocol.HEAD_FILE, downloadFileName)

        mySocket.send(request)

        with open(self.conf.clientDownloadPath+"/"+downloadFileName, "wb") as f:
            while True:
                data = mySocket.recv(1024)
                if not data:
                    break
                f.write(data)
            print(downloadFileName+" has been downloaded!")
            mySocket.close()
    

    def uploadFile(self, uploadFileName):
        mySocket = self.connect()
        request = Protocol.prepareMessage(Protocol.HEAD_UPLOAD, uploadFileName)   
        mySocket.send(request)


        header, msg = Protocol.decodeMessage(mySocket.recv(1024).decode())

        if (header == Protocol.HEAD_READY):
            f=open(self.conf.clientSharePath + "/"  + uploadFileName, 'rb')
            l=f.read(1024)
            while(l):
                mySocket.send(l)
                l=f.read(1024)
        else:
            print("Upload Failed: \nHeader: ",header," \nMessage: ",msg)
            

    # Main logic of the client

    def start(self):

        selection = 0

        while selection != 4:
            selection = self.getUserSelection()

            if selection == 1:
                self.getDownloadFileList()
                self.printDownloadFileList()
                print("Get the file list")
            elif selection == 2:
              
                fileName = self.selectDownloadFile()
                print("Downloading file")
                self.downloadFile(fileName)
              
            elif selection == 3:

                fileName = self.selectUploadFile()
                print("Uploading file: " + fileName)
                self.uploadFile(fileName)
            else:
                pass

# Entry point

def main():
    c = Client()
    c.start()

if __name__ == '__main__':
    main()