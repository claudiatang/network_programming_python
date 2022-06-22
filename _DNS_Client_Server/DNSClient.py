import socket

def main():
    serverName = 'localhost'
    serverPort = 13500
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    try:
        while True:
            hostnameInput = input('Enter hostname to be looked up: ')
            try:
                clientSocket.sendto(hostnameInput.encode(), (serverName,serverPort))
            except socket.error as e:
                print(e)
                break
            
            try:
                recvRecord, serverAddr = clientSocket.recvfrom(4096)
                print(recvRecord.decode())
            except socket.error as e:
                print(e)
                break

            input('Press \'Ctrl + C\' to exit or\nPress \'Enter\' to continue.\n>>')
    
    except KeyboardInterrupt:
        pass
    
    clientSocket.close()
    print("DNS client socket closed")

if __name__ == '__main__':
    main()