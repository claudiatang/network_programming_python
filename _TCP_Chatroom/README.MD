### Introduction
- This is a simple chatroom app using on TCP connection. It aims to implement a client-server architecture that allows multiple clients connect to a single server and communicate with the others via the server.
### How to run scripts
- The program is composed of two scripts:
  - [ChatroomServer.py](https://github.com/claudiatang/network_programming_python/blob/main/TCP_chatroom/ChatroomServer.py) as the chatroom server, and 
  - [ChatroomClient.py](https://github.com/claudiatang/network_programming_python/blob/main/TCP_chatroom/ChatroomClient.py) as a client
- In the first terminal use command ```python ChatroomServer.py``` to launch the chatroom server and keep it on. 
- In another terminal, use command ```python ChatroomClient.py``` to run a client. Enter chatroom server IP address when prompted. Enter client nickname to be used in the chatroom when prompted.
Once successfully connected to the chatroom server, the client will be prompted "Connect to remote successful" and is able to start chatting
- Multiple clients can be connected to the chatroom server
### Chatroom architecture
- 

### Python threading
- Both the server and the client program use threading to enable sending messages to the server and listening on a port to receive messages simultaneously.
- 