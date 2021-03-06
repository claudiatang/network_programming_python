### Introduction
- The [DNSServer.py](https://github.com/claudiatang/network_programming_python/blob/main/DNS_client_server/DNSServer.py) and [DNSClient.py](https://github.com/claudiatang/network_programming_python/blob/main/DNS_client_server/DNSClient.py) scripts look into implementing DNS lookup function by querying a server running on the loopback address.
- Learning objectives:
  - understand loopback interface and loopback data flow process
  - send DNS query using UDP as layer 4 protocol
  - understand and implement blocking/non-blocking socket
### How to run scripts

- The program is composed of two scripts:
   - [DNSServer.py](https://github.com/claudiatang/network_programming_python/blob/main/DNS_client_server/DNSServer.py) as the DNS server, and
   - [DNSClient.py](https://github.com/claudiatang/network_programming_python/blob/main/DNS_client_server/DNSClient.py) as a DNS client
- To use the DNS query function from the client:
  - Open two terminals. 
  - In the first terminal, use command ```python DNSServer.py``` to launch the DNS server and keep the server on. Once the server is successfully launched and ready to receive queries, the program prints "DNS server is ready ..." on the terminal.
  - In the second terminal, use command ```python DNSClient``` to run the DNS client program. Once the client is on, type a remote host name as instructed to query for its IPv4 and Cname record.
- To terminate the program:
   - Exit the server: press "Ctrl + C" anytime 
   - Exit the client: press "Ctrl + C" after a query

### DNS query data flow
- Loopback interface
The client script has hardcoded the remote DNS server as ```serverName = "localhost"```. This string host name equals to the special IPv4 address ```127.0.01``` where the client will send the queried host name. 
Data sent through loopback interface is contained inside the same host, which means our DNS client and server communication is conducted inside the host that runs the [DNSServer.py](https://github.com/claudiatang/network_programming_python/blob/main/DNS_client_server/DNSServer.py) and [DNSClient.py](https://github.com/claudiatang/network_programming_python/blob/main/DNS_client_server/DNSClient.py) scripts.
- The DNS server program, once receiving a queried host name from a client, is responsible for querying any higher level DNS servers (e.g. a gateway router's DNS component) by calling ```socket.getaddrinfo()``` ([reference link](https://docs.python.org/3/library/socket.html#socket.getaddrinfo))
- A diagram illustrating the loopback + DNS query process<br><br>
  <img src="https://github.com/claudiatang/network_programming_python/blob/main/img/loopback_dns_lookup.png"  width="600" height="auto">

### Blocking and non-blocking socket
- This refers to whether the I/O function of a socket block the execution of other tasks.<br>
Here is a brilliant article [Understanding Non Blocking I/O with Python ??? Part 1](https://medium.com/vaidikkapoor/understanding-non-blocking-i-o-with-python-part-1-ec31a2e2db9b) on blocking/non-blocking I/O using TCP socket as example.<br>
Our [DNSServer.py](https://github.com/claudiatang/network_programming_python/blob/main/DNS_client_server/DNSServer.py) needs a non-blocking UDP socket, so that the listening function ```socket.recvfrom()``` will not block the execution of other part of the code when there is no data received from any client. This is necessary as we need the "Ctrl + C" keyboard interruption function to close the running server.<br>
After the UDP socket has been created and bind, the ```serverSocket.setblocking(0)``` function is called to set the socket to non-blocking.<br>
When a non-blocking socket does not have any data available, it throws socket.error exception instead of blocking the program.Therefore, a ```try ... except ...``` block is needed to handle the error, and if the error is of [BlockingIIOError](https://docs.python.org/3/library/exceptions.html#BlockingIOError) type, the program should continue to the next round of the loop.
