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
        if sys.platform.startswith("win"):
            output = subprocess.Popen(["ping", "-n", "1", ip_addr], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
        elif sys.platform.startswith("linux"):
            output = subprocess.Popen(['/bin/ping','-c 1',ip_addr],stdout = subprocess.PIPE).communicate()[0]
        output = output.decode("utf-8")
        #print(f"Output {output}")
        if not "unreachable" in output:
            print(f"The Ip Address {ip_addr} has responded with a ECHO_REPLY!")
except KeyboardInterrupt:
    print("Scan has been terminated ...")