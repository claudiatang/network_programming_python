### Command format

&emsp;&ensp;The command format for pinging a remote server is:\
&emsp;&ensp;`python ping.py <hostname>`

### Flow of the pinging functionality

### Functions

- #### Calculate checksum

  `def calChecksum(packet)`

- #### Construct echo request

  `def constructEchoRequest(icmp_type, icmp_code, pid, seq_num, pld_size)`

- #### Send echo request

  `def sendEchoRequest (ping_socket: skt.socket, echo_req_pkt, remote_ip)`

- #### Receive echo reply
  `def rcvEchoReply(default_timeout, start_time, ping_socket: skt.socket, pid)`
