import socket
import PacketParser as pparser

def main():
    HOST = socket.gethostbyname(socket.gethostname())
    linRawSock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    
    try:
        while True:
            rawData, addr = linRawSock.recvfrom(65565)
            ether_header = pparser.get_ether_header(rawData[:14])
            print(f"# Ethernet header info:")
            print(f"  dest mac: {ether_header[0]}")
            print(f"  source mac: {ether_header[1]}")
            print(f"  ethernet protocol: {ether_header[2]}")
            
            ip_header = pparser.get_ip_addr(rawData[14:34])
            print(f"## IP header info:")
            print(f"   IP version: {ip_header[0]}")
            ip_ihl = ip_header[1]*32/8
            print(f"   IP header len: {ip_ihl}")
            print(f"   IP upper layer proto: {ip_header[6]}")
            print(f"   IP addresses: src {ip_header[7]} --> dest {ip_header[8]}")
            
            if int(ip_header[6]) == 1:
                icmp_header = pparser.get_icmp_header(rawData[20:28])
                print(f"### ICMP header fields:")
                print(f"    ICMP type: {icmp_header[0]}")
                print(f"    ICMP code: {icmp_header[1]}")
                print(f"    ICMP checksum: {icmp_header[2]} {len(icmp_header[2])}")
                print(f"    pid: {icmp_header[3]}")
                print(f"    sequence number: {icmp_header[4]}")
                
            if int(ip_header[6]) == 6:
                tcp_header = pparser.get_tcp_header(rawData[20:40])
                print(f"### TCP header fields:")
                print(f"    TCP src port: {tcp_header[0]}")
                print(f"    TCP dest port: {tcp_header[1]}")
                print(f"    TCP seq num: {tcp_header[2]}")
                print(f"    TCP ack num: {tcp_header[3]}")
                print(f"    TCP data offset: {tcp_header[4]}")
                print(f"    TCP reserved: {tcp_header[5]}")
                print(f"    TCP flags:")
                for flag, val in zip(["nonce", "cwr", "ecn_echo", "urgent", "ack", "push", "reset", "syn", "fin"], tcp_header[6]):
                    print(f"     TCP flag {flag}: {val}")
                print(f"    TCP window size: {tcp_header[7]}")
                print(f"    TCP checksum: {tcp_header[8]}")
                print(f"    TCP urgent point: {tcp_header[9]}")
            
    
    except KeyboardInterrupt:
        pass
    
    
    linRawSock.close()
    print("Sniffer stops!")



    
if __name__ == '__main__':
    main()

