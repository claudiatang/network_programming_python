import struct
import socket

def get_ether_header(eth_header_14):
    eth_header = struct.unpack('!6s6sH', eth_header_14)
    dest_mac = get_mac_addr(eth_header[0])
    src_mac = get_mac_addr(eth_header[1])
    proto_type = socket.htons(eth_header[2])
    return dest_mac, src_mac, proto_type

def get_mac_addr(addr_bytes_obj):
    addr_sections = map(lambda x: format(x, '02x'), addr_bytes_obj)
    #addrSections = map('{:02x}'.format, bytesObj)
    return ':'.join(addr_sections)

def get_ip_header(ip_header_20):
    ip_header = struct.unpack('!BBHHHBBH4s4s', ip_header_20)
    ip_ver = int((0b011110000 & ip_header[0])/16)
    # ihl value represents the number of 32-bit words in the header
    # the actual bytes is calculated as ihl*32/8
    ihl = int(0b000001111 & ip_header[0])
    tos = format(ip_header[1], 'd')
    total_len = format(ip_header[2], 'd')
    idf = format(ip_header[3], 'd')
    ttl = format(ip_header[5],'d')
    upper_l_proto = format(ip_header[6], 'd')
    src_ip = get_ip_addr(ip_header[8])
    dest_ip = get_ip_addr(ip_header[9])
    return ip_ver, ihl, tos, total_len, idf, ttl, upper_l_proto, src_ip, dest_ip

def get_ip_addr(addr_bytes_obj):
    addr_sections = map(lambda x: format(x, 'd'), addr_bytes_obj)
    return '.'.join(addr_sections)

def get_icmp_header(icmp_header_8):
    icmp_header = struct.unpack('!BBHHH', icmp_header_8)
    icmp_type = int(icmp_header[0])
    icmp_code = int(icmp_header[1])
    checksum = bin(icmp_header[2])
    pid = int(icmp_header[3])
    seq_num = int(icmp_header[4])
    return icmp_type, icmp_code, checksum, pid, seq_num

def get_tcp_header(tcp_header_20):
    tcp_header = struct.unpack('!HHLLBBHHH', tcp_header_20)
    src_port = int(tcp_header[0])
    dest_port = int(tcp_header[1])
    tcp_seq = int(tcp_header[2])
    tcp_ack = int(tcp_header[3])
    data_offset = bin(int((0b01111000000000000 & tcp_header[4])/4096))
    reserved = bin(int((0b00000111000000000 & tcp_header[4])/512))
    control_flags = get_tcp_flags(0b00000000111111111 & tcp_header[4])
    win_size = int(tcp_header[5])
    checksum = bin(tcp_header[6])
    urg_pnt = tcp_header[7]
    return src_port, dest_port, tcp_seq, tcp_ack, data_offset, reserved, control_flags, win_size, checksum, urg_pnt
    
def get_tcp_flags(flag_bits_9):
    nonce =    bool(0b0100000000 & flag_bits_9)
    cwr =      bool(0b0010000000 & flag_bits_9)
    ecn_echo = bool(0b0001000000 & flag_bits_9)
    urgent =   bool(0b0000100000 & flag_bits_9)
    ack =      bool(0b0000010000 & flag_bits_9)
    push =     bool(0b0000001000 & flag_bits_9)
    reset =    bool(0b0000000100 & flag_bits_9)
    syn =      bool(0b0000000010 & flag_bits_9)
    fin =      bool(0b0000000001 & flag_bits_9)
    return nonce, cwr, ecn_echo, urgent, ack, push, reset, syn, fin
    