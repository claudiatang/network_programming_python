# simple sniffer on windows code example from https://docs.python.org/3/library/socket.html
# the public network interface
import socket
import struct
import pcap
import dpkt

def main():
    HOST = socket.gethostbyname(socket.gethostname())
    
    pc = pcap.pcap(name=None, promisc=True, immediate=True, timeout_ms=50)
    decode = {pcap.DLT_LOOP:dpkt.loopback.Loopback, pcap.DLT_NULL:dpkt.loopback.Loopback, pcap.DLT_EN10MB:dpkt.ethernet.Ethernet}[pc.datalink()]
    
    try:
        print(f"Listening on {pc.name}: {pc.filter}")
        for ts, pkt in pc:
            raw_data = str(decode(pkt))
            dest_mac, src_mac, eth_proto = get_ether_header(raw_data[:14])

            print('\nEthernet Frame:')
            print(f"Destination MAC: {dest_mac}")
            print(f"Source MAC: {src_mac}")
            print(f"Protocol: {eth_proto}")
    except KeyboardInterrupt:
        nrecv, ndrop = pc.stats()
        print(f"\n{nrecv} packets received by filter")
        print(f"{ndrop} packets dropped by kernel")
    
    print("Sniffer stops!")


def get_ether_header(rawHeader):
    ether_header = struct.unpack('!6s6sH', rawHeader)
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

def get_ip_header(rawData):
    ip_header = struct.unpack('!BBHHHBBH4s4s', rawData[:20])
    version = int((0b011110000 & ip_header[0])/16)
    ihl = 0b000001111 & ip_header[0]
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

