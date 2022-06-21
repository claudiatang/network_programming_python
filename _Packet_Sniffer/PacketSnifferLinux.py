#!/usr/bin/env python

import socket
import PacketParser as pparser

def main():
    HOST = socket.gethostbyname(socket.gethostname())
    linux_raw_sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    
    try:
        while True:
            raw_data, addr = linux_raw_sock.recvfrom(65565)
            ether_header = pparser.get_ether_header(raw_data[:14])
            print(f"# Ethernet header info:")
            print(f"  dest mac: {ether_header[0]}")
            print(f"  source mac: {ether_header[1]}")
            print(f"  ethernet protocol: {ether_header[2]}")
            
            ip_ver, ihl, tos, total_len, idf, ttl, upper_l_proto, src_ip, dest_ip = pparser.get_ip_header(raw_data[14:34])
            print(f"## IP header info:")
            print(f"   IP version: {ip_ver}")
            print(f"   IP header len: {ihl*32/8}")
            print(f"   IP upper layer proto: {upper_l_proto}")
            print(f"   IP addresses: src {src_ip} --> dest {dest_ip}")
            
            if int(upper_l_proto) == 1:
                icmp_header = pparser.get_icmp_header(raw_data[34:42])
                print(f"### ICMP header fields:")
                print(f"    ICMP type: {icmp_header[0]}")
                print(f"    ICMP code: {icmp_header[1]}")
                print(f"    ICMP checksum: {icmp_header[2]} {len(icmp_header[2])}")
                print(f"    pid: {icmp_header[3]}")
                print(f"    sequence number: {icmp_header[4]}")
                
            if int(upper_l_proto) == 6:
                tcp_header = pparser.get_tcp_header(raw_data[34:54])
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
    
    
    linux_raw_sock.close()
    print("Sniffer stops!")



    
if __name__ == '__main__':
    main()

