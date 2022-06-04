from http import server
import socket as skt

def main():
    serverName = 'localhost'
    serverPort = 13500
    clientSocket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)
    
    try:
        while True:
            hostnameInput = input('Enter hostname to be looked up: ')
            clientSocket.sendto(hostnameInput.encode(), (serverName,serverPort))
            recvRecord, serverAddr = clientSocket.recvfrom(4096)
            print(recvRecord.decode())
            continueQuery = bool(input('Do you want to query another hostname?\nInput any characters to continue.\nPress \'Enter\' only to exit.\n>>'))
    except KeyboardInterrupt:
        pass
    
    clientSocket.close()
    print("DNS client socket closed")

if __name__ == '__main__':
    main()