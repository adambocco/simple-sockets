
# define the protocol header

HEAD_REQUEST="REQ"
HEAD_FILE="FIL"
HEAD_ERROR="ERR"
HEAD_UPLOAD="UPL"
HEAD_READY="RDY"

# prepare the message

def prepareMessage(header, message):
    return (header+message).encode()

def prepareFileList(header, fileList):
    message = header
    
    for i in range(len(fileList)):

        if (i==len(fileList)-1):
            message+=fileList[i]
        else:
            message+=fileList[i]+","
    
    return message.encode()

def decodeMessage(message):
    if (len(message) <3):
        return HEAD_ERROR, "EMPTY MESSAGE"
    else:
        return message[0:3], message[3:len(message)]