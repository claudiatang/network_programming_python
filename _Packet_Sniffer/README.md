### packet sniffer on windows and linux
- socket is platform based<br>
- raw socket provided by python socket can capture ethernet packets on linux
- on windows system, raw socket functions provided by python socket module can only capture ip packets. For capturing ethernet frames on windows, pypcap library is needed. WinPcap developer's pack is needed, which is the industry-standard tool for link layer access in Windows environment
