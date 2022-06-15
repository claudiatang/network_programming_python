# simple sniffer on windows code example from https://docs.python.org/3/library/socket.html
# the public network interface
import socket
import struct

def main():
    HOST = socket.gethostbyname(socket.gethostname())

    # create a raw socket and bind it to the public interface
    winRawSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
    #LinuxSocket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))

    # Include IP headers
    #winRawSocket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    winRawSocket.bind((HOST,0))
    winRawSocket.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    # receive all packages
    try: 
        while True:
            winRawSocket.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

            # receive a package
            rawData, addr = winRawSocket.recvfrom(65565)
            #dlHeader = data_link_header(rawData)
            ipHeader = ip_header(rawData)
            #print(f"data link layer header: {dlHeader}")
            print(f"ip header ihl: {ipHeader[1]}")
            print(f"ip header total length: {ipHeader[3]}")
            print(f"ip header ttl: {ipHeader[5]}")
            print(f"ip header protocol: {ipHeader[6]}")
            print(f"ip addresses: {ipHeader[7]} --> {ipHeader[8]}")
            #print(rawData)
            # disabled promiscuous mode
            winRawSocket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    except KeyboardInterrupt:
        pass
    
    
    winRawSocket.close()
    print("Sniffer stops!")


def data_link_header(rawData):
    ether_header = struct.unpack('!6s6sH', rawData[:14])
    #print(f"d: {d}")
    #print(f"s: {s}")
    #print(f"p: {p}")
    destMac = mac_addr(ether_header[0])
    srcMac = mac_addr(ether_header[1])
    protoType = socket.htons(ether_header[2])
    #print(f"destMac: {destMac}")
    #print(f"srcMac: {srcMac}")
    #print(f"protoType: {protoType}")
    return destMac, srcMac, protoType

def mac_addr(bytesObj):
    addrSections = map(lambda x: format(x, '02x'), bytesObj)
    #addrSections = map('{:02x}'.format, bytesObj)
    return ':'.join(addrSections)

def ip_header(rawData):
    ip_header = struct.unpack('!BBHHHBBH4s4s', rawData[:20])
    version = (0b011110000 & ip_header[0])/16
    ihl = 0b000001111 & ip_header[0]
    tos = format(ip_header[1], 'd')
    totalLen = format(ip_header[2], 'd')
    idf = format(ip_header[3], 'd')
    ttl = format(ip_header[5],'d')
    proto = format(ip_header[6], 'd')
    srcIP = ip_addr(ip_header[8])
    destIP = ip_addr(ip_header[9])
    return version, ihl, tos, totalLen, idf, ttl, proto, srcIP, destIP

def ip_addr(bytesObj):
    addrSections = map(lambda x: format(x, 'd'), bytesObj)
    return '.'.join(addrSections)
    
    
    
    
if __name__ == '__main__':
    main()

