import socket as skt

# simple sniffer on windows code example from https://docs.python.org/3/library/socket.html
# the public network interface
HOST = skt.gethostbyname(skt.gethostname())

# create a raw socket and bind it to the public interface
WinSocket = skt.socket(skt.AF_INET, skt.SOCK_RAW, skt.IPPROTO_IP)
#LinuxSocket = skt.socket(skt.AF_PACKET, skt.SOCK_RAW, skt.ntohs(3))

# Include IP headers
WinSocket.setsockopt(skt.IPPROTO_IP, skt.IP_HDRINCL, 1)

# receive all packages
WinSocket.ioctl(skt.SIO_RCVALL, skt.RCVALL_ON)

# receive a package
print(WinSocket.recvfrom(65565))

# disabled promiscuous mode
WinSocket.ioctl(skt.SIO_RCVALL, skt.RCVALL_OFF)

