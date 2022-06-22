#!/usr/bin/env python

from ast import Str
import threading
import socket
import sys

def main():
    serverIP = getIPAddr("Enter chatroom server IPv4 address: ")
    serverPort = 49152
    clientNickname = getString("Enter your chatroom nickname (10 letters maximum): ", 10)
    

    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            clientSocket.connect((serverIP, serverPort))
            print('Connect to remote successful.')
            clientSocket.send(clientNickname.encode())
            break
        except socket.error as e:
            print(e)
    
    sending_thread = threading.Thread(target=clientSendMsg, args=(clientSocket,))
    recving_thread = threading.Thread(target=clientRecvMsg, args=(clientSocket,))
    
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
                socket.inet_aton(IP)
                return IP
        except socket.error:
            print("Not a legal IPv4 address")
            
def getPortNum(min: int, max: int, prompt: str):
    port = 0
    while port<min or port>max:
        try:
            port = int(input(prompt))
        except socket.error:
            print("Not a legal port number")
    return port

def clientSendMsg(clientSocket: socket.socket):
    try:
        while True:
            msg_send = takeMsg()
            try:
                if msg_send == 'exit':
                    clientSocket.shutdown(socket.SHUT_RDWR)
                    clientSocket.close()
                    break
                clientSocket.send(msg_send.encode())
            except socket.error as e:
                print(e)
                break
    except KeyboardInterrupt:
        clientSocket.shutdown(socket.SHUT_RDWR)
        clientSocket.close()
        print("Terminate connection by keyboard interruption.\nClient is leaving.")
    
def clientRecvMsg(clientSocket: socket.socket):
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