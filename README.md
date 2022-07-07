## Low-level Network Programming in Python
This is a study repository of network programming in python3 
### Description
Programs in this repository are written in python3, aiming to dissect the anatomy and investigate the functionalities of protocol data units (PDUs) of some common protocols in TCP/IP network architecture.
For study purpose, library chosen are limited to python's built-in low-level networking interface and binary data construct/deconstruct libraries (such as socket and struct), while python modules that already provide packet manipulation (such as scapy) are not used.

### Contents
Each program looks into some particular topics in network programming and provides explanation on code and related algorithm. Please refer to below links for detailed contents
- [DNS Client Server Program](https://github.com/claudiatang/network_programming_python/tree/main/DNS_client_server)
  - stateless connection in python
  - loopback interface
  - blocking/non-blocking socket
- [Ping Remote Server Program](https://github.com/claudiatang/network_programming_python/tree/main/ping)
  - checksum calculation
  - ICMP message format
  - header information retrieval
- [Network Scanner Program](https://github.com/claudiatang/network_programming_python/tree/main/_Network_Scanner)
  - run another program as a subprocess in python 
  - command line arguments manager using python argparse module
- [Port Scanner Program](https://github.com/claudiatang/network_programming_python/tree/main/_Port_Scanner)
  - probe whether specified tcp ports of a remote host is open or closed 
  - more argparse module functions
- [Packet Sniffer Program](https://github.com/claudiatang/network_programming_python/tree/main/_Packet_Sniffer)
  - create raw socket to receive ethernet packets
  - parse network packet headers on different network layers
- [TCP Chatroom Program](https://github.com/claudiatang/network_programming_python/tree/main/TCP_chatroom)
  - stateful connection in python
  - multi threading to allow listening and sending simultaneously
- [P2P Chatting Program](https://github.com/claudiatang/network_programming_python/tree/main/_Peer_to_Peer_Simple)

### Dependencies 
python3 standard libraries.
Please refer to [the official website](https://www.python.org/downloads/) for downloading and installing python3.  
