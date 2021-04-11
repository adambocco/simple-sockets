
class Config:
    serverConfig="Server.txt"
    clientConfig="Client.txt"

    def __init__(self):
        self.readClientConfig()
        self.readServerConfig()

    def readServerConfig(self):
        try:
            with open(self.serverConfig, 'r') as f:
                for l in f:
                    print(l)
                    sub=l.strip().split("=")
                    if (sub[0] == "SERVER_PORT"):
                        self.serverPort = int(sub[1])
                    elif (sub[0] =="PATH"):
                        self.sharedPath = sub[1]
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
                    elif (sub[0] =="PATH"):
                        self.downloadPath = sub[1]
                    else:
                        pass
        except:
            print( Exception.message() )
                    


def test():
    c = Config()

test()