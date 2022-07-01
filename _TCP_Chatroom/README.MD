### Introduction
- This is a simple chatroom app using TCP connection. It aims to implement a client-server architecture that allows multiple clients connect to a single server, with each client able to receive messages from all other clients via the server.
### How to run scripts
- The program is composed of two scripts:
  - [ChatroomServer.py](https://github.com/claudiatang/network_programming_python/blob/main/TCP_chatroom/ChatroomServer.py) as the chatroom server, and 
  - [ChatroomClient.py](https://github.com/claudiatang/network_programming_python/blob/main/TCP_chatroom/ChatroomClient.py) as a client
- Open the 1st terminal as the chatroom server. 
  Use command ```python ChatroomServer.py``` to launch the server and keep it on. 
- Open another terminal as a client. 
  Use command ```python ChatroomClient.py``` to run a client.
  Enter chatroom server IP address when prompted.
  Enter client nickname to be used in the chatroom when prompted.
  Once successfully connected to the chatroom server, the client will be prompted "Connect to remote successful" and is able to start sending messages
- Multiple clients can be connected to the chatroom server
### Chatroom architecture
-  A diagram illustrating the chatroom client-server architecture and how messages flow
  <img src="https://github.com/claudiatang/network_programming_python/blob/main/img/chatroom_client_server.png"  width="600" height="auto">

### Python threading
- The client program uses threading to enable sending messages to the server and listening on the port to receive messages simultaneously.
- The server program creates a new thread for each connected client, and kill the thread when that client drops. 