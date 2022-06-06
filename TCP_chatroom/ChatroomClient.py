from ast import Str
import threading as thd
import socket as skt
import sys

def main():
    serverIP = getIPAddr("Enter chatroom server IPv4 address: ")
    serverPort = 49152
    clientNickname = getString("Enter your chatroom nickname (10 letters maximum): ", 10)
    

    clientSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
    while True:
        try:
            clientSocket.connect((serverIP, serverPort))
            print('Connect to remote successful.')
            clientSocket.send(clientNickname.encode())
            break
        except skt.error as e:
            print(e)
    
    sending_thread = thd.Thread(target=clientSendMsg, args=(clientSocket,))
    recving_thread = thd.Thread(target=clientRecvMsg, args=(clientSocket,))
    
    sending_thread.start()
    recving_thread.start()
    sending_thread.join()

    sys.exit()

def getString(prompt: Str, maxLen: int):
    inputStr = ""
    while inputStr=="" or len(inputStr)>maxLen:
        inputStr=input(prompt)
    return inputStr
        
    
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

def clientSendMsg(clientSocket: skt.socket):
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
    
def clientRecvMsg(clientSocket: skt.socket):
    while True:
        try:
            msg_recv = clientSocket.recv(1024).decode()
            if msg_recv == "test_if_sock_is_still_open":
                continue
            else:
                msg_display = "<<"+msg_recv
                print()
                print(colored(255,128,0,msg_display)+"\n>>", end='')
        except:
            print("exit client recv...")
            break

def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)        


if __name__ == '__main__':
    main()