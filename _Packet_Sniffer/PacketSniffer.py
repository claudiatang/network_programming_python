# simple sniffer on windows code example from https://docs.python.org/3/library/socket.html
# the public network interface
import socket
import PacketParser as pparser

def main():
    HOST = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
    print(HOST)

    
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
            print("# Network Layer header fields:")
            print(f"  IP version: {ipHeader[0]}")
            print(f"  header length: {ipHeader[1]} 32-bit words = {int((ipHeader[1]*32/8))} bytes")
            print(f"  Packet total length: {ipHeader[3]}")
            print(f"  TTL: {ipHeader[5]}")
            print(f"  Upper layer protocol: {ipHeader[6]}")
            print(f"  ip addresses: src:{ipHeader[7]} --> dest:{ipHeader[8]}")
            
            #print ICMP header
            if int(ipHeader[6]) == 1:
                icmp_header = pparser.get_icmp_header(rawData[20:28])
                print("## ICMP header fields:")
                print(f"   ICMP type: {icmp_header[0]}")
                print(f"   ICMP code: {icmp_header[1]}")
                print(f"   ICMP checksum: {icmp_header[2]} {len(icmp_header[2])}")
                print(f"   pid: {icmp_header[3]}")
                print(f"   sequence number: {icmp_header[4]}")
                
            #print TCP header
            if int(ipHeader[6]) == 6:
                tcp_header = pparser.get_tcp_header(rawData[20:40])
                print("## TCP header fields:")
                print(f"   TCP src port: {tcp_header[0]}")
                print(f"   TCP dest port: {tcp_header[1]}")
                print(f"   TCP seq num: {tcp_header[2]}")
                print(f"   TCP ack num: {tcp_header[3]}")
                print(f"   TCP data offset: {tcp_header[4]}")
                print(f"   TCP reserved: {tcp_header[5]}")
                print(f"   TCP flags:")
                for flag, val in zip(["nonce", "cwr", "ecn_echo", "urgent", "ack", "push", "reset", "syn", "fin"], tcp_header[6]):
                    print(f"     TCP flag {flag}: {val}")
                print(f"   TCP window size: {tcp_header[7]}")
                print(f"   TCP checksum: {tcp_header[8]}")
                print(f"   TCP urgent point: {tcp_header[9]}")
            
            # disabled promiscuous mode
            winRawSocket.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
            
            
                
    except KeyboardInterrupt:
        pass
    
    
    winRawSocket.close()
    print("Sniffer stops!")

if __name__ == '__main__':
    main()

