import os
import sys
import socket as skt
import struct
import time
import select

def main():
    dest_IP = ""
    if len(sys.argv) != 2:
        sys.exit('Command format error.\nPlease use correct format: python ping.py <hostname>')
    try:
        dest_IP = skt.gethostbyname(sys.argv[1])
    except:
        sys.exit('Provided host name not found')
    
    print(f"Ping destination {dest_IP} in Python")
    
    ECHOREQ_TYPE = 8
    ECHOREQ_CODE = 0
    ECHOREQ_PLD_SIZE = 32
    TIMEOUT = 4
    PROCESS_ID = os.getpid()&0xffff
    print(PROCESS_ID)
    DEFAULT_PING_NUM = 4
    
    for i in range(DEFAULT_PING_NUM):
        try:
            socket = skt.socket(skt.AF_INET,skt.SOCK_RAW, skt.getprotobyname("icmp"))
        except skt.error as e:
            print("Create ICMP socket failed with error: ", end='')
            print(e)
        echo_req_pkt = constructEchoRequest(ECHOREQ_TYPE, ECHOREQ_CODE, PROCESS_ID, i, ECHOREQ_PLD_SIZE)
        start_time = sendEchoRequest(socket, echo_req_pkt, dest_IP)
        if(start_time >= 0):
            rcvEchoReply(TIMEOUT, start_time, socket, PROCESS_ID)
        socket.close()
        #print("socket closed")
        


def calChecksum(packet):
    sum = 0
    count = (int(len(packet)/2))*2 
    i = 0
    while i<count:
        #check memory byte order "little-endian" or "big-endian" 
        #https://getkt.com/blog/endianness-little-endian-vs-big-endian/
        if(sys.byteorder == "little"):
            # multiplied by 256 == append 8 "0"s at end of the binary number
            sub_sum=packet[i+1]*256+packet[i] 
        else:
            sub_sum = packet[i]*256+packet[i+1]
        sum = sum+sub_sum
        i = i+2
    # when packet has odd number of bytes
    if count<len(packet):
        sum = sum+packet[len(packet)-1]
    # make binary of sum 32 bit long 
    sum &= 0xffffffff
    # sum>>16: the 1 bit carry on the 16th position
    # sum&0xffff : get the 17~32th bits
    # wrap around the carry and add to the rightmost position
    sum=(sum>>16)+(sum&0xffff)
    # convert 16 bit integer from host to network byte order
    checksum = skt.htons(~sum&0xffff)
    return checksum
    
def constructEchoRequest(icmp_type, icmp_code, pid, seq_num, pld_size):
    checksum = 0
    header = struct.pack("!BBHHH", icmp_type, icmp_code, checksum, pid, seq_num)
    pld_bytes = []
    for x in range(0x7, 0x7 + pld_size):
        pld_bytes += [(x & 0xff)]
    payload = bytes(pld_bytes)
    
    checksum = calChecksum(header + payload)
    header = struct.pack("!BBHHH", icmp_type, icmp_code, checksum, pid, seq_num)
    #print("echo request constructed")
    return header+payload

def sendEchoRequest (ping_socket: skt.socket, echo_req_pkt, remote_ip):
    try:
        ping_socket.sendto(echo_req_pkt, (remote_ip,1))
        start_time = time.time()
        #print("echo request sent")
        return start_time
    except skt.error as e:
        print("Send echo request failed: ", end='')
        print(e.args[1])
        ping_socket.close()
        return float(-1.0)

def rcvEchoReply(default_timeout, start_time, ping_socket: skt.socket, pid):
    while True:
        ready = select.select([ping_socket],[],[], default_timeout)
        if ready[0] == []:
            print("Request timed out!")
            return
        
        rcv_echo_reply, addr = ping_socket.recvfrom(4096)
        rcv_time = time.time()
        # get spent time in milliseconds
        spent_time = (rcv_time - start_time)*1000
        header_names = ["type","code","checksun","pid","seq"]
        header_bytes = rcv_echo_reply[20:28]
        header_unpack = struct.unpack("!BBHHH",header_bytes)
        header_dict = dict(zip(header_names,header_unpack))
        if header_dict["pid"] == pid:
            ip_header_names = ["version", "type", "length","id", "flags", "ttl", "protocol","checksum", "src", "dest"]
            ip_header_bytes = rcv_echo_reply[:20]
            ip_header_unpack = struct.unpack("!BBHHHBBHII",ip_header_bytes)
            ip_header_dict = dict(zip(ip_header_names,ip_header_unpack))
            
            # payload size = whole reply packet size - ip header size - icmp header size
            seq_num = header_dict["seq"]
            size = len(rcv_echo_reply)-28
            ttl = ip_header_dict["ttl"]
            
            
            print(f"Reply from {addr[0]}: bytes={size} time={spent_time: .2f}ms sequence_number={seq_num} TTL={ttl}")
            return
            
        


        

if __name__ == '__main__':
    main()