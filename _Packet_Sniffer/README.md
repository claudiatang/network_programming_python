### Introduction
- This program sniffs network packets that to and from the local host, and parses the packets' header information according to corresponding network protocols
### packet sniffer on windows and linux
- raw socket created by python socket module is platform based<br>
  - on a linux system, the raw socket can capture from ethernet frames and upper layer packets
  - on windows system, the raw socket can only capture packets from network layer and upper. 
  in order to capture ethernet frames on windows, pypcap library is needed. 
  And in order to install pypcap, WinPcap developer's pack is needed, which is the industry-standard tool for link layer access in Windows environment (but this topic is out of the scope of this project)
