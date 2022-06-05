import threading as thd
import socket as skt

def main():
    serverIP = getIPAddr("Enter chatroom server IPv4 address: ")
    serverPort = 49152

    clientSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
    while True:
        try:
            clientSocket.connect((serverIP, serverPort))
            print('Connect to remote successful.')
            break
        except skt.error as e:
            print(e)
            
    try:
        while True:
            msg_send = takeMsg()
            try:
                if msg_send == 'exit':
                    clientSocket.shutdown(skt.SHUT_RDWR)
                    clientSocket.close()
                    break
                clientSocket.send(msg_send.encode())
            except skt.error as e:
                print(e)
                break
    except KeyboardInterrupt:
        clientSocket.shutdown(skt.SHUT_RDWR)
        clientSocket.close()
        print("Terminate connection by keyboard interruption.\nClient is leaving.")
    
def takeMsg():
    inputMsg = ""
    while True:
        inputMsg = input('>> ')
        if len(inputMsg)>=1024:
            print("message is too long! Failed to send.")
        else:
            return inputMsg    

def getIPAddr(prompt):
    IP = ""
    while True:
        try:
            IP = input(prompt)
            if IP=="localhost":
                return IP
            else:
                skt.inet_aton(IP)
                return IP
        except skt.error:
            print("Not a legal IPv4 address")
            
def getPortNum(min: int, max: int, prompt: str):
    port = 0
    while port<min or port>max:
        try:
            port = int(input(prompt))
        except skt.error:
            print("Not a legal port number")
    return port

def clientSendMsg(clientSocket):
    while True:
        msg_send = input('>>')
        try:
            # socket.send() is used for TCP SOCK_STREAM connected sockets
            # socket.sendto() is used for UDP SOCK_DGRAM unconnected datagram sockets
            clientSocket.send(msg_send.encode())
            if msg_send == 'byebye':
                break
        except:
            print("Break due to sending to server error.")
            break
    
        


if __name__ == '__main__':
    main()