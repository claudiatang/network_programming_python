from msilib.schema import Error
import socket
import argparse
import threading
import io
from contextlib import redirect_stderr


def main():
    parser = argparse.ArgumentParser(description = "Scan open ports on specified host")
    parser.add_argument("--ip", "-ip", help="host IP address <exp. 192.168.0.1>", type=str, required=True)
    
    mx_group = parser.add_mutually_exclusive_group()
    mx_group.add_argument("--port", "-p", help="number of ports to scan. mutually exclusive to --count/-c", type=int, choices=range(1,65536), metavar="range: 1 to 65535 inclusive", required=False)
    mx_group.add_argument("--count", "-c", help="number of ports to scan. mutually exclusive to --port/-p", type=int, choices=range(1,65536), metavar="range: 1 to 65535 inclusive", required=False)
    
    cli_args = None
    
    try:
        f = io.StringIO()
        with redirect_stderr(f):
            cli_args = parser.parse_args()
    except:
        print("usage: PortScanner.py [-h] --ip IP [--port range: 1 to 65535 inclusive | --count range: 1 to 65535 inclusive]\ninvalid argument(s) detected\nrefer to \'PortScanner.py [-h]\' for correct usage of command line arguments")
        exit(1)

    host_ip = cli_args.ip
    port_cnt = cli_args.count
    port = cli_args.port

    print(f"host_ip {host_ip}")
    print(f"port_cnt {port_cnt}")
    print(f"port {port}")
    
    if (port_cnt is None) and (port is None):
        print(f"do a full port scan to {host_ip}")
        try:
            for p in range(1,65536):
                new_thread = threading.Thread(target=scan_port, args=(host_ip,p))
                #new_thread.daemon = True
                new_thread.start()
        except KeyboardInterrupt:
            print("user terminated the program")
            exit(1)
    else:
        if port_cnt is None:
            scan_port(host_ip, port)
        else:
            for p in range(1, port_cnt+1):
                new_thread = threading.Thread(target=scan_port, args=(host_ip,p))
                #new_thread.daemon = True
                new_thread.start()
            
    
def scan_port(ip, port):
    sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    #sock.setblocking(0)
    if sock.connect_ex((ip, port)):
        sock.close()
    else:
        print(f"tcp/{port}    open")
        sock.close()

        
if __name__ == '__main__':
    main()
