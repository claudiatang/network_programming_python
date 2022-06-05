import sys
import errno
import socket as skt
import threading as thd
from time import sleep

def main():
    serverPort = 49152
    serverSocket = skt.socket(skt.AF_INET, skt.SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(5)
    print("Chatroom is open now!")
    

    while True:
        try:
            connectionSocket, addr = serverSocket.accept()
            if connectionSocket != None:
                new_thread = thd.Thread(target=serverRecv, args=(connectionSocket,))
                new_thread.daemon = True
                new_thread.start()
        except skt.error as e:
            print("*******************************************************************")
            print(e)
        
    sys.exit()


def serverRecv(connectionSocket: skt.socket):
    while True:
        try:
            connectionSocket.send(("ok").encode())
            msg_recv = connectionSocket.recv(1024).decode()
            print(connectionSocket)
            print('<<<'+ msg_recv)  
        except skt.error as e:
            print(e)
            break




if __name__ == '__main__':
    main()