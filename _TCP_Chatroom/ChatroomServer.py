#!/usr/bin/env python

import sys
#import errno
import socket
import threading
#from time import sleep

def main():
    serverPort = 49152
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.bind(('', serverPort))
    serverSocket.listen(5)
    print("Chatroom is open now!")
    
    liveSockets = {}
    try:
        while True:
            try:
                #printLiveSockets(liveSockets)
                connectionSocket, addr = serverSocket.accept()
                nickname = connectionSocket.recv(10).decode()
                #print(nickname)
                if connectionSocket != None:
                    liveSockets[nickname] = connectionSocket
                    #liveSockets[str(connectionSocket.getpeername()[1])] = connectionSocket
                    new_thread = threading.Thread(target=serverRecv, args=(connectionSocket, liveSockets, nickname))
                    new_thread.daemon = True
                    new_thread.start()
            except socket.error as e:
                print("*******************************************************************")
                print(e)
    except KeyboardInterrupt:
        print("Server is closing ...")
        
    sys.exit()

def printLiveSockets(liveSockets):
    for x in liveSockets:
        print(x)

def serverRecv(connectionSocket: socket.socket, liveSockets, nickname):
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
                    #liveSockets[key].send(("You: "+msg_recv).encode())
                    continue
                else:
                    liveSockets[key].send((f"{nickname}: "+msg_recv).encode())
        except Exception as ex:
            #print(ex)
            #printLiveSockets(liveSockets)
            print(f"{nickname} is leaving ...")
            del liveSockets[nickname]
            #connectionSocket.shutdown(socket.SHUT_RDWR)
            #connectionSocket.close()
            break




if __name__ == '__main__':
    main()