### Command format

&emsp;&emsp;The command format for pinging a remote server is:\
&emsp;&emsp;`python ping.py <hostname>`

### Flow of the pinging functionality
![ping-flow-chart](https://github.com/claudiatang/network_programming_python/blob/main/ping/img/ping_flow_chart.png?raw=true)
### Functions

- #### Calculate checksum

  `def calChecksum`
  | parameter(s) ||
  |--------------|-|
  |packet: ||

- #### Construct echo request

  `def constructEchoRequest(icmp_type, icmp_code, pid, seq_num, pld_size)`
  | parameter(s) ||
  |--------------|-|
  |icmp_type: ||
  |icmp_code:||
  |pid:||
  |seq_num:||
  |pld_size:||

- #### Send echo request

  `def sendEchoRequest (ping_socket: skt.socket, echo_req_pkt, remote_ip)`
  | parameter(s) ||
  |--------------|-|
  |ping_socket: ||
  |echo_req_pkt:||
  |remote_ip:||

- #### Receive echo reply
  `def rcvEchoReply(default_timeout, start_time, ping_socket: skt.socket, pid)`
  | parameter(s) | |
  |--------------|-|
  |icmp_type: ||
  |icmp_code:||
  |pid:||
  |seq_num:||
  |pld_size:||
