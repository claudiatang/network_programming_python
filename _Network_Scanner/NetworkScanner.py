#!/usr/bin/env python

import subprocess
import sys
import argparse

parser = argparse.ArgumentParser(description = "Scan devices on LAN")
parser.add_argument("-network",dest="network", help="LAN address <exp. 192.168.2>", type=str, required=True)
#parser.add_argument("-machines",dest="machines", help="number of machines", type=int, required=True)

parsed_args = parser.parse_args()

for ip in range(1,255):
    ip_addr = parsed_args.network + '.' + str(ip)
    print(f"Scanning {ip_addr}")
    output = subprocess.Popen(["python", "/home/claudia/Github/network_programming_python/_Ping/ping.py", ip_addr], stdout=subprocess.PIPE).communicate()[0]
    output = output.decode("utf-8")
    print(f"Output {output}")
    if "Lost = 0" in output or "bytes from " in output:
        print(f"The Ip Address {ip_addr} has responded with a ECHO_REPLY!")