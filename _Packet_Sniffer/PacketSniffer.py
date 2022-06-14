# simple sniffer on windows code example from https://docs.python.org/3/library/socket.html
# the public network interface
import socket as skt
import struct

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
            recved_obj = winRawSocket.recvfrom(65534)
            #print(recved_obj)
            #for x in recved_obj:
            #    print(type(x))
            #    print(len(x))
            dlHeader = data_link_header(recved_obj[0])
            print(f"data link layer header: {dlHeader}")
            # disabled promiscuous mode
            winRawSocket.ioctl(skt.SIO_RCVALL, skt.RCVALL_OFF)
    except KeyboardInterrupt:
        pass
    
    
    winRawSocket.close()
    print("Sniffer stops!")

def data_link_header(packet):
    d, s, p = struct.unpack('!6s6sH', packet[:14])
    #print(f"d: {d}")
    #print(f"s: {s}")
    #print(f"p: {p}")
    destMac = mac_addr(d)
    srcMac = mac_addr(s)
    protoType = skt.htons(p)
    #print(f"destMac: {destMac}")
    #print(f"srcMac: {srcMac}")
    #print(f"protoType: {protoType}")
    return destMac, srcMac, protoType

def mac_addr(bytesObj):
    addrSections = map(lambda x: format(x, '02x'), bytesObj)
    return ':'.join(addrSections)
    
    
    
if __name__ == '__main__':
    main()

