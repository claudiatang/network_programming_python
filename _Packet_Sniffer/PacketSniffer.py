# simple sniffer on windows code example from https://docs.python.org/3/library/socket.html
# the public network interface
import socket
import PacketParser as pparser

def main():
    HOST = socket.gethostbyname(socket.gethostname())

    
    # create a raw socket and bind it to the public interface
    winRawSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW)
    winRawSocket.bind((HOST,0))
    
    # Include IP headers
    winRawSocket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    
    try: 
        while True:
            # receive all packages
            winRawSocket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

            # receive a package
            rawData, addr = winRawSocket.recvfrom(65565)
            #dlHeader = get_ether_header(rawData)
            ipHeader = pparser.get_ip_header(rawData[:20])
            #print(f"data link layer header: {dlHeader}")
            print("Network Layer header fields:")
            print(f"   IP version: {ipHeader[0]}")
            print(f"   header length: {ipHeader[1]} 32-bit words = {int((ipHeader[1]*32/8))} bytes")
            print(f"   Packet total length: {ipHeader[3]}")
            print(f"   TTL: {ipHeader[5]}")
            print(f"   Upper layer protocol: {ipHeader[6]}")
            print(f"   ip addresses: src:{ipHeader[7]} --> dest:{ipHeader[8]}")
            #print(rawData)
            # disabled promiscuous mode
            winRawSocket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    except KeyboardInterrupt:
        pass
    
    
    winRawSocket.close()
    print("Sniffer stops!")

if __name__ == '__main__':
    main()

