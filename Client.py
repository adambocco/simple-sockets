import Protocol
import Config
import os
from socket import *


class Client:
    
    def __init__(self):
        self.conf = Config.Config()

    # Function to print out user menu

    def printMenu(self):
        print("Welcome to Simple File Sharing System!")
        print("Please select an operation from the menu: ")
        print("=========================================")
        print("1. View the List of Available Files")
        print("2. Download File")
        print("3. Quit")
        print("=========================================")
    
    # Function to get user selection from the menu

    def getUserSelection(self):
        selection = 0

        while selection > 3 or selection < 1:
            self.printMenu()
            try:
                selection = int(input())
            except:
                selection=0
            if (selection <=3 and selection >=1):
                return selection
            print("Invalid Option")

    # Build connection to the server

    def connect(self):
        clientSocket = socket(AF_INET, SOCK_STREAM)
        clientSocket.connect((self.conf.serverName, self.conf.serverPort))
        return clientSocket

    # Function to get file list from the server
    
    def getFileList(self):
        mySocket=self.connect()
        
        request = Protocol.prepareMessage(Protocol.HEAD_REQUEST, "")
        mySocket.send(request)

        header, msg = Protocol.decodeMessage(mySocket.recv(1024).decode())

        mySocket.close()

        if (header == Protocol.HEAD_REQUEST):
            files = msg.split(",")
            self.fileList = []
            for f in files:
                self.fileList.append(f)

    # Function to print out file names

    def printFileList(self):
        
        for i,f in enumerate(self.fileList):
            print('{:<3d}{}'.format(i, f))


    # Function to let user to select a file from the list

    def selectDownloadFile(self):
        if (len(self.fileList) == 0):
            self.getFileList()
        ans = -1
        while (ans < 0 or ans > len(self.fileList)):
            self.printFileList()
            print("Please select the file you want to download (Enter the number of the file)")
            try:
                ans = int(input())
            except:
                ans = -1
            if (ans >= 0 and ans < len(self.fileList)):
                return self.fileList[ans]
            print("Invalid number")

    # Function to download file

    def downloadFile(self, fileName):
        mySocket = self.connect()
        request = Protocol.prepareMessage(Protocol.HEAD_FILE, fileName)

        mySocket.send(request)

        with open(self.conf.downloadPath+"/"+fileName, "wb") as f:
            while True:
                data = mySocket.recv(1024)
                if not data:
                    break
                f.write(data)
            print(fileName+" has been downloaded!")
            mySocket.close()
    
    # Main logic of the client

    def start(self):

        selection = 0

        while selection != 3:
            selection = self.getUserSelection()

            if selection == 1:
                self.getFileList()
                self.printFileList()
                print("Get the file list")
            elif selection == 2:
              
                fileName = self.selectDownloadFile()
                print("Downloading file")
                self.downloadFile(fileName)
              
            else:
                pass

# Entry point

def main():
    c = Client()
    c.start()

if __name__ == '__main__':
    main()