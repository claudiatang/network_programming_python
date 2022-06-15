import socket
import struct

def main():
    HOST = socket.gethostbyname(socket.gethostname())
    linRawSock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    
    try:
        while True:
            rawData, addr = linRawSock.recvfrom(65565)
            dest_mac, src_mac, eth_proto = data_link_header(rawData)
            print(f"dest mac: {dest_mac}")
            print(f"source mac: {src_mac}")
            print(f"ethernet protocol: {eth_proto}")
            
    
    except KeyboardInterrupt:
        pass
    
    
    linRawSock.close()
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
    version = int((0b011110000 & ip_header[0])/16)
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

