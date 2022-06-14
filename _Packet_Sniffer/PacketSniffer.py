# simple sniffer on windows code example from https://docs.python.org/3/library/socket.html
# the public network interface
import socket as skt

def main():
    HOST = skt.gethostbyname(skt.gethostname())

    # create a raw socket and bind it to the public interface
    winRawSocket = skt.socket(skt.AF_INET, skt.SOCK_RAW, skt.IPPROTO_IP)
    #LinuxSocket = skt.socket(skt.AF_PACKET, skt.SOCK_RAW, skt.ntohs(3))

    # Include IP headers
    winRawSocket.setsockopt(skt.IPPROTO_IP, skt.IP_HDRINCL, 1)
    winRawSocket.bind((HOST,65534))

    # receive all packages
    try: 
        while True:
            winRawSocket.ioctl(skt.SIO_RCVALL, skt.RCVALL_ON)

            # receive a package
            print(winRawSocket.recvfrom(65534))

            # disabled promiscuous mode
            winRawSocket.ioctl(skt.SIO_RCVALL, skt.RCVALL_OFF)
    except KeyboardInterrupt:
        pass
    
    
    winRawSocket.close()
    print("Sniffer stops!")
    
    
if __name__ == '__main__':
    main()

