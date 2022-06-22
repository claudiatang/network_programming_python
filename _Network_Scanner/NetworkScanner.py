#!/usr/bin/env python

import subprocess
import sys
import argparse

parser = argparse.ArgumentParser(description = "Scan devices on LAN")
parser.add_argument("-nw",dest="network", help="Network address <exp. 192.168.2>", type=str, required=True)
#parser.add_argument("-machines",dest="machines", help="number of machines", type=int, required=True)

parsed_args = parser.parse_args()

try:
    for ip in range(1,255):
        ip_addr = parsed_args.network + '.' + str(ip)
        print(f"Scanning {ip_addr}")
        output = subprocess.Popen(["python", "..\_Ping\ping.py", ip_addr], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        output = output.decode("utf-8")
        #print(f"Output {output}")
        if not "unreachable" in output:
            print(f"IP Address {ip_addr} has responded with a ECHO_REPLY!")
except KeyboardInterrupt:
    print("Scan has been terminated ...")