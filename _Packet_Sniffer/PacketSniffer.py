#!/usr/bin/env python

# simple sniffer on windows code example from https://docs.python.org/3/library/socket.html
# the public network interface
import socket
import sys
import PacketParser as pparser

def main():
    HOST = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
    print(HOST)
    
    is_win = None
    if sys.platform.startswith("win"):
        is_win = True
        # create a raw socket and bind it to the public interface
        raw_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW)
        raw_sock.bind((HOST,0))
        
        # Include IP headers
        raw_sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
        # receive all packages
        raw_sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    elif sys.platform.startswith("linux"):
        is_win = False
        raw_sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(3))
    
    
        
    try: 
        while True:

            # receive a package
            raw_data, addr = raw_sock.recvfrom(65565)
            
            if is_win:
                ip_ver, ihl, tos, total_len, idf, ttl, upper_l_proto, src_ip, dest_ip = pparser.get_ip_header(raw_data[:20])
                print()
                print_ip_header(ip_ver, ihl, total_len, ttl, upper_l_proto, src_ip, dest_ip)
                if int(upper_l_proto) == 1:
                    icmp_type, icmp_code, checksum, pid, seq_num = pparser.get_icmp_header(raw_data[20:28])
                    print_icmp_header(icmp_type, icmp_code, checksum, pid, seq_num)
                if int(upper_l_proto) == 6:
                    src_port, dest_port, tcp_seq, tcp_ack, data_offset, reserved, control_flags, win_size, checksum, urg_pnt = pparser.get_tcp_header(raw_data[20:40])
                    print_tcp_header(src_port, dest_port, tcp_seq, tcp_ack, data_offset, reserved, control_flags, win_size, checksum, urg_pnt)
                if int(upper_l_proto) == 17:
                    src_port, dest_port, length, checksum = pparser.get_udp_header(raw_data[20:28])
                    print_udp_header(src_port, dest_port, length, checksum)
                
                
                    
            elif not is_win:
                dest_mac, src_mac, eth_type = pparser.get_ether_header(raw_data[:14])
                ip_ver, ihl, tos, total_len, idf, ttl, upper_l_proto, src_ip, dest_ip = pparser.get_ip_header(raw_data[14:34])
                print()
                print_eth_header(dest_mac, src_mac, eth_type)
                print_ip_header(ip_ver, ihl, total_len, ttl, upper_l_proto, src_ip, dest_ip)
                if int(upper_l_proto) == 1:
                    icmp_type, icmp_code, checksum, pid, seq_num = pparser.get_icmp_header(raw_data[34:42])
                    print_icmp_header(icmp_type, icmp_code, checksum, pid, seq_num)
                if int(upper_l_proto) == 6:
                    src_port, dest_port, tcp_seq, tcp_ack, data_offset, reserved, control_flags, win_size, checksum, urg_pnt = pparser.get_tcp_header(raw_data[34:54])
                    print_tcp_header(src_port, dest_port, tcp_seq, tcp_ack, data_offset, reserved, control_flags, win_size, checksum, urg_pnt)
                if int(upper_l_proto) == 17:
                    src_port, dest_port, length, checksum = pparser.get_udp_header(raw_data[34:42])
                    print_udp_header(src_port, dest_port, length, checksum)
                
            else:
                print("Unknown platform. Exit!")
                break

    except KeyboardInterrupt:
        pass
    
    # disabled promiscuous mode
    if is_win:
        raw_sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    raw_sock.close()
    print("Sniffer stops!")

def print_eth_header(dest_mac, src_mac, eth_type ):
    print(f"# Ethernet header info:")
    print(f"  dest mac: {dest_mac}")
    print(f"  source mac: {src_mac}")
    print(f"  ethernet type: {eth_type}")

def print_ip_header(ip_ver, ihl, total_len, ttl, upper_l_proto, src_ip, dest_ip):
    print(f"  ## Network Layer header fields:")
    print(f"     IP version: {ip_ver}")
    print(f"     header length: {ihl} 32-bit words = {int((ihl*32/8))} bytes")
    print(f"     Packet total length: {total_len}")
    print(f"     TTL: {ttl}")
    print(f"     Upper layer protocol: {upper_l_proto}")
    print(f"     ip addresses: src:{src_ip} --> dest:{dest_ip}")
    
def print_icmp_header(icmp_type, icmp_code, checksum, pid, seq_num):
    print(f"     ### ICMP header fields:")
    print(f"         ICMP type: {icmp_type}")
    print(f"         ICMP code: {icmp_code}")
    print(f"         ICMP checksum: {checksum}")
    print(f"         pid: {pid}")
    print(f"         sequence number: {seq_num}")
    
def print_tcp_header(src_port, dest_port, tcp_seq, tcp_ack, data_offset, reserved, control_flags, win_size, checksum, urg_pnt):
    print(f"     ### TCP header fields:")
    print(f"         TCP src port: {src_port}")
    print(f"         TCP dest port: {dest_port}")
    print(f"         TCP seq num: {tcp_seq}")
    print(f"         TCP ack num: {tcp_ack}")
    print(f"         TCP data offset: {data_offset}")
    print(f"         TCP reserved: {reserved}")
    print(f"         TCP flags:")
    for flag, val in zip(["nonce", "cwr", "ecn_echo", "urgent", "ack", "push", "reset", "syn", "fin"], control_flags):
        print(f"            TCP flag {flag}: {val}")
    print(f"         TCP window size: {win_size}")
    print(f"         TCP checksum: {checksum}")
    print(f"         TCP urgent point: {urg_pnt}")
    
def print_udp_header(src_port, dest_port, length, checksum):
    print(f"     ### UDP header fields:")
    print(f"         UDP src port: {src_port}")
    print(f"         UDP dest port: {dest_port}")
    print(f"         UDP segment length: {length}")
    print(f"         UDP checksum: {checksum}")
    
    
    

if __name__ == '__main__':
    main()

