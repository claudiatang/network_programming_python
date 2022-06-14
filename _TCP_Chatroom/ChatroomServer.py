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
            #printLiveSockets(liveSockets)
            connectionSocket, addr = serverSocket.accept()
            nickname = connectionSocket.recv(10).decode()
            #print(nickname)
            if connectionSocket != None:
                liveSockets[nickname] = connectionSocket
                #liveSockets[str(connectionSocket.getpeername()[1])] = connectionSocket
                new_thread = thd.Thread(target=serverRecv, args=(connectionSocket, liveSockets, nickname))
                new_thread.daemon = True
                new_thread.start()
        except skt.error as e:
            print("*******************************************************************")
            print(e)
        
    sys.exit()

def printLiveSockets(liveSockets):
    for x in liveSockets:
        print(x)

def serverRecv(connectionSocket: skt.socket, liveSockets, nickname):
    while True:
        try:
            connectionSocket.send(("test_if_sock_is_still_open").encode())
            msg_recv = connectionSocket.recv(1024).decode()
            #print(connectionSocket)
            #print(connectionSocket.getpeername()[1])
            print(f"{nickname}: "+ msg_recv)
            #printLiveSockets(liveSockets)
            for key in liveSockets:
                if key == nickname:
                    liveSockets[key].send(("You: "+msg_recv).encode())
                else:
                    liveSockets[key].send((f"{nickname}: "+msg_recv).encode())
        except skt.error as e:
            #print(e)
            #printLiveSockets(liveSockets)
            print(f"{nickname} is leaving ...")
            del liveSockets[nickname]
            connectionSocket.shutdown(skt.SHUT_RDWR)
            connectionSocket.close()
            break




if __name__ == '__main__':
    main()