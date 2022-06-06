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
    
    liveSockets = {}
    while True:
        try:
            printLiveSockets(liveSockets)
            connectionSocket, addr = serverSocket.accept()
            if connectionSocket != None:
                liveSockets[str(connectionSocket.getpeername()[1])] = connectionSocket
                new_thread = thd.Thread(target=serverRecv, args=(connectionSocket, liveSockets))
                new_thread.daemon = True
                new_thread.start()
        except skt.error as e:
            print("*******************************************************************")
            print(e)
        
    sys.exit()

def printLiveSockets(liveSockets):
    for x in liveSockets:
        print(x)

def serverRecv(connectionSocket: skt.socket, liveSockets):
    while True:
        try:
            connectionSocket.send(("").encode())
            msg_recv = connectionSocket.recv(1024).decode()
            print(connectionSocket)
            print(connectionSocket.getpeername()[1])
            print('<<<'+ msg_recv)
            printLiveSockets(liveSockets)
            for socket in liveSockets:
                liveSockets[socket].send(('<<<'+ msg_recv).encode())
        except skt.error as e:
            #print(e)
            printLiveSockets(liveSockets)
            del liveSockets[str(connectionSocket.getpeername()[1])]
            connectionSocket.shutdown(skt.SHUT_RDWR)
            connectionSocket.close()
            break




if __name__ == '__main__':
    main()