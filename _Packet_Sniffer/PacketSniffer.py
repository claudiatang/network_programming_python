# simple sniffer on windows code example from https://docs.python.org/3/library/socket.html
# the public network interface
import socket
import struct
import pcap

def main():
    HOST = socket.gethostbyname(socket.gethostname())

    
    # create a raw socket and bind it to the public interface
    winRawSocket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)
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
            ipHeader = get_ip_header(rawData[:20])
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


def get_ether_header(rawData):
    ether_header = struct.unpack('!6s6sH', rawData[:14])
    #print(f"d: {d}")
    #print(f"s: {s}")
    #print(f"p: {p}")
    destMac = get_mac_addr(ether_header[0])
    srcMac = get_mac_addr(ether_header[1])
    protoType = socket.htons(ether_header[2])
    #print(f"destMac: {destMac}")
    #print(f"srcMac: {srcMac}")
    #print(f"protoType: {protoType}")
    return destMac, srcMac, protoType

def get_mac_addr(bytesObj):
    addrSections = map(lambda x: format(x, '02x'), bytesObj)
    #addrSections = map('{:02x}'.format, bytesObj)
    return ':'.join(addrSections)

def get_ip_header(rawHeader):
    ip_header = struct.unpack('!BBHHHBBH4s4s', rawHeader)
    version = int((0b011110000 & ip_header[0])/16)
    # ihl value represents the number of 32-bit words in the header
    # the actual bytes is calculated as ihl*32/8
    ihl = int(0b000001111 & ip_header[0])
    tos = format(ip_header[1], 'd')
    totalLen = format(ip_header[2], 'd')
    idf = format(ip_header[3], 'd')
    ttl = format(ip_header[5],'d')
    proto = format(ip_header[6], 'd')
    srcIP = get_ip_addr(ip_header[8])
    destIP = get_ip_addr(ip_header[9])
    return version, ihl, tos, totalLen, idf, ttl, proto, srcIP, destIP

def get_ip_addr(bytesObj):
    addrSections = map(lambda x: format(x, 'd'), bytesObj)
    return '.'.join(addrSections)
    
    
    
    
if __name__ == '__main__':
    main()

