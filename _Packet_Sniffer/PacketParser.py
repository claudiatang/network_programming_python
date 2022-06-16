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