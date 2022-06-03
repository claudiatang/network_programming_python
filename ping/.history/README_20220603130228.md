### Command format

&emsp;&emsp;The command format for pinging a remote server is:\
&emsp;&emsp;`python ping.py <hostname>`

### Flow of the pinging functionality

```flow
st=>start: Start
cond=>condition: Reached
maxium pinging
number?
suba=>subroutine: Create raw socket
for ICMP
subb=>subroutine: Construct
ICMP echo request
subc=>subroutine: Send echo request
subd=>subroutine: Receive echo reply
sube=>subroutine: Close raw socket
e=>end

st->cond->suba
cond(no)->suba(right)->subb(right)->subc(right)->subd(right)->sube(right)->cond()
cond(yes)->e
```

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
