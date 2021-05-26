import os


class Config:
    serverConfig="Server.txt"
    clientConfig="Client.txt"

    def __init__(self, configType):
        if configType == self.serverConfig:
            if os.path.exists(self.serverConfig):
                self.readServerConfig()
            else:
                print("Server configuration file does not exist.")
        elif configType == self.clientConfig:
            if os.path.exists(self.clientConfig):
                self.readClientConfig()
            else:
                print("Client configuration file does not exist.")
        else:
            print("Invalid configuration type")


    def readServerConfig(self):
        try:
            with open(self.serverConfig, 'r') as f:
                for l in f:
                    print(l)
                    sub=l.strip().split("=")
                    if (sub[0] == "SERVER_PORT"):
                        self.serverPort = int(sub[1])
                    elif (sub[0] =="SERVER_DOWNLOAD_PATH"):
                        self.serverDownloadPath = sub[1]
                    elif (sub[0] =="SERVER_SHARE_PATH"):
                        self.serverSharePath = sub[1]
                    else:
                        pass
        except:
            print( Exception.message() )

    def readClientConfig(self):
        try:
            with open(self.clientConfig, 'r') as f:
                              
                for l in f:
                    print(l)
                    sub=l.strip().split("=")
                    if (sub[0] == "SERVER_PORT"):
                        self.serverPort = int(sub[1])
                    elif (sub[0] =="CLIENT_PORT"):
                        self.clientPort = int(sub[1])
                    elif (sub[0] =="SERVER"):
                        self.serverName = sub[1]
                    elif (sub[0] =="CLIENT_DOWNLOAD_PATH"):
                        self.clientDownloadPath = sub[1]
                    elif (sub[0] =="CLIENT_SHARE_PATH"):
                        self.clientSharePath = sub[1]
                    else:
                        pass
        except:
            print( Exception.message() )
                    