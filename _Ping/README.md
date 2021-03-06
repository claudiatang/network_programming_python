### Introduction
- This [ping.py](https://github.com/claudiatang/network_programming_python/blob/main/ping/ping.py) script aims to carry out a study on layer 3 PDU anatomy and the ping functionality, rather than fully replicating the ```ping``` command and its various flags used in CLI.
- Learning objectives:
  - implement checksum calculation using python built-in bytes type
  - assemble ICMP packet as per [RFC 792](https://datatracker.ietf.org/doc/html/rfc792) specification
  - dissemble IP packet and retrieve header information

### How to run the script

&emsp;&emsp;The command format for pinging a remote server from Windows or Linux CLI is:\
&emsp;&emsp;`python ping.py <hostname>`

### Flow of the pinging functionality

<img src="https://github.com/claudiatang/network_programming_python/blob/main/img/ping_flow_chart.png"  width="400" height="auto">

### Functions

- #### Calculate checksum

  `def calChecksum(packet)`
  | parameter(s) |type|description|
  |-|-|-|
  |packet|_bytes_|bytes object of header+payload|
  - Checksum calculation uses the common checksum algorithm that is also adopted by many other protocols including IP, UDP and TCP.
  The algorithm adds together every two 16-bit words, and wraps around the final carry to be added to the sum. This is illustrated in the following figure:
  <br><img src="https://github.com/claudiatang/network_programming_python/blob/main/img/checksum_algorithm.png" width="400" height="auto"><br>
  - python bytes object is a sequence of single byte (8 bits) that can be accessed by indexes, so every 2 bytes need to be appended together to form a 16-bit word in checksum calculation.
  This is done by ```word = byte_1*256 + byte_2```, where ```byte_1*256``` appends 8 zeros at the end of byte_1.
  - The function also takes in consideration different [endianness]("https://getkt.com/blog/endianness-little-endian-vs-big-endian/") (byte orders) of different computer systems, which decides the order of which the function appends two bytes. The endianness information is obtained by ```sys.byteorder```
  - The wrap-around step is done by
  first, converting the word to 32-bit long ```sum &= 0xffffffff```
  then,  take the 16th bit from the left ```sum>>16```
  add this bit to the last 16 bits of the 32-bit long word ```(sum>>16)+(sum&0xffff)```, which equals to wrapping around the carry and adding it to the sum
  - The sum needs to be converted from host to network byte order using ```socket.htons()``` before finally returned as checksum value


- #### Construct echo request

  `def constructEchoRequest(icmp_type, icmp_code, pid, seq_num, pld_size)`
  | parameter(s) |type|description|
  |-|-|-|
  |icmp_type|_numeric literal:<br>integer_|echo request type = 8|
  |icmp_code|_numeric literal:<br>integer_|echo request code = 0|
  |pid|_int_|current process ID number|
  |seq_num|_int_|sequence number of pings&emsp;&emsp;&emsp;&emsp;|
  |pld_size|_numeric literal:<br>integer_|size of payload|
  
  |return(s)|type&emsp;&emsp;&emsp;&emsp;&ensp;|description|
  |-|-|-|
  |echo request&nbsp;|_bytes_|echo request packet in bytes format|

  - The construction of echo request message is as per the ICMP format specified in the "Echo Reply Message" section of [RFC 792](https://datatracker.ietf.org/doc/html/rfc792).
  - ```struct.pack(format, v1, v2, ...)``` ([reference link](https://docs.python.org/3/library/struct.html#struct.pack)) is used to pack up passed in fields according to the [format](https://docs.python.org/3/library/struct.html#format-characters) argument. ( Note that the identifier field takes the binary value of current process id formatted to fit into the size of 2 bytes)
  - Fields need to be packed twice:
  When packed up for the 1st time, value of the checksum field is 0.
  After this 1st pack-up, ```calChecksum()``` function is called to calculate the checksum value using the bytes object acquired from the 1st pack-up.
  Then, with the calculated checksum value, all fields are being packed up for the 2nd time to construct the final echo request message message
  - The constructed echo request message is the return value of this function.
  


- #### Send echo request

  `def sendEchoRequest (ping_socket, echo_req_pkt, remote_ip)`
  | parameter(s) |type|description|
  |-|-|-|
  |ping_socket|_socket_|raw socket for ICMP message|
  |echo_req_pkt|_bytes_|constructed echo request bytes object|
  |remote_ip|_string_|remote server IP address|

  |return(s)&emsp;&emsp;|type&ensp;&nbsp;|description|
  |-|-|-|
  |start_time|_float_|time stamp at the point of sending<br>(return -1.0 when failing to send)&emsp;&emsp;&ensp;|
  - The function captures the time when the ```socket.sendto()``` function has run without error. This float type time value is the function return value when sending is successful.
  While sending fails, the functions returns -1.0

- #### Receive echo reply
  `def rcvEchoReply(default_timeout, start_time, ping_socket, pid)`
  | parameter(s) |type||
  |-|-|-|
  |default_timeout|_numeric literal:<br>integer_|timeout value|
  |start_time|_float_|start time stamp captured at the point of sending|
  |ping_socket|_socket_|raw socket for ICMP datagram|
  |pid|_int_|current process ID number|
  - ping has a timeout value for receiving echo reply from the remote server.
  This is handled by calling ```select.select()``` ([reference link](https://docs.python.org/3/library/select.html#select.select)) from python's select module, and setting its ```timeout``` value.
  When this value is reached without receiving any message from remote server, the program prints "Request timed out!" and return.
  - If a packet is received before time out, the time of receiving the packet is then captured. RTT value is calculated by subtracting the passed in sending time (captured and returned by ```sendEchoRequest()``` function) from receiving time.
  -  The received ICMP message is encapsulated in an IP datagram where the 21-28th bytes ```[20:28]``` are the ICMP header. Once extracted, the ICMP header bytes object is unpacked using ```struct.unpack()``` into fields using the same format as packing an ICMP message.
  Sequence number is obtained from the last field.
  The received identifier (process ID) is compared with the sent identifier value to decided whether the reply is from an expected server.
  - The first 20 bytes ```[:20]``` are the IP header. Once extracted, the IP header is also unpacked according to IP header format ```"!BBHHHBBHII"```, from which TTL value is obtained.
  - remote server IP, received packet length, RTT, sequence number and TTL are printed to the terminal
