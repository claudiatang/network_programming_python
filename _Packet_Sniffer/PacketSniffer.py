# simple sniffer on windows code example from https://docs.python.org/3/library/socket.html
# the public network interface
import socket
import PacketParser as pparser

def main():
    HOST = socket.gethostbyname_ex(socket.gethostname())[-1][-1]
    print(HOST)

    
    # create a raw socket and bind it to the public interface
    win_raw_sock = socket.socket(socket.AF_INET, socket.SOCK_RAW)
    win_raw_sock.bind((HOST,0))
    
    # Include IP headers
    win_raw_sock.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
    # receive all packages
    win_raw_sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)
    
    try: 
        while True:
            

            # receive a package
            raw_data, addr = win_raw_sock.recvfrom(65565)
            #dlHeader = get_ether_header(raw_data)
            ip_ver, ihl, tos, total_len, idf, ttl, upper_l_proto, src_ip, dest_ip = pparser.get_ip_header(raw_data[:20])
            #print(f"data link layer header: {dlHeader}")
            print("# Network Layer header fields:")
            print(f"  IP version: {ip_ver}")
            print(f"  header length: {ihl} 32-bit words = {int((ihl*32/8))} bytes")
            print(f"  Packet total length: {total_len}")
            print(f"  TTL: {ttl}")
            print(f"  Upper layer protocol: {upper_l_proto}")
            print(f"  ip addresses: src:{src_ip} --> dest:{dest_ip}")
            
            #print ICMP header
            if int(upper_l_proto) == 1:
                icmp_type, icmp_code, checksum, pid, seq_num = pparser.get_icmp_header(raw_data[20:28])
                print("## ICMP header fields:")
                print(f"   ICMP type: {icmp_type}")
                print(f"   ICMP code: {icmp_code}")
                print(f"   ICMP checksum: {checksum}")
                print(f"   pid: {pid}")
                print(f"   sequence number: {seq_num}")
                
            #print TCP header
            if int(upper_l_proto) == 6:
                src_port, dest_port, tcp_seq, tcp_ack, data_offset, reserved, control_flags, win_size, checksum, urg_pnt = pparser.get_tcp_header(raw_data[20:40])
                print("## TCP header fields:")
                print(f"   TCP src port: {src_port}")
                print(f"   TCP dest port: {dest_port}")
                print(f"   TCP seq num: {tcp_seq}")
                print(f"   TCP ack num: {tcp_ack}")
                print(f"   TCP data offset: {data_offset}")
                print(f"   TCP reserved: {reserved}")
                print(f"   TCP flags:")
                for flag, val in zip(["nonce", "cwr", "ecn_echo", "urgent", "ack", "push", "reset", "syn", "fin"], control_flags):
                    print(f"     TCP flag {flag}: {val}")
                print(f"   TCP window size: {win_size}")
                print(f"   TCP checksum: {checksum}")
                print(f"   TCP urgent point: {urg_pnt}")
                
    except KeyboardInterrupt:
        pass
    
    # disabled promiscuous mode
    win_raw_sock.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
    win_raw_sock.close()
    print("Sniffer stops!")

if __name__ == '__main__':
    main()

