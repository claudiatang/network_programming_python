## Low-level Network Programming in Python
This is a study repository of network programming in python3 
### Description
Programs in this repository are written in python3, aiming to dissect the anatomy and investigate the functionalities of protocol data units (PDUs) of some common protocols in TCP/IP network architecture.
For study purpose, library chosen are limited to python's built-in low-level networking interface and binary data construct/deconstruct libraries (such as socket and struct), while python modules that already provide packet manipulation (such as scapy) are not used.

### Contents
Each program looks into some particular topics in network programming and provides explanation on code and related algorithm. Please refer to below links for detailed contents
- [DNS Client Server Program](https://github.com/claudiatang/network_programming_python/tree/main/DNS_client_server)
  - loopback interface
  - blocking/non-blocking socket
- [Ping Remote Server Program](https://github.com/claudiatang/network_programming_python/tree/main/ping)
  - checksum calculation
  - ICMP message format
  - header information retrieval

### Dependencies 
python3 standard libraries.
Please refer to [the official website](https://www.python.org/downloads/) for downloading and installing python3.  
