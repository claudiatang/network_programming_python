import socket
import argparse
import threading


def main():
    parser = argparse.ArgumentParser(description = "Scan open ports on specified host")
    parser.add_argument("--ip", "-ip", dest="host", help="host IP address <exp. 192.168.0.1>", type=str, required=True)
    parser.add_argument("--port", "-p", dest="port", help="number of ports to scan", type=int, required=False)
    parser.add_argument("--count", "-c", dest="count", help="number of ports to scan", type=int, required=False)

    host_ip = parser.parse_args().host
    port_cnt = 0
    port = 0
    
    if parser.parse_args().port:
        port = parser.parse_args().port
        port_cnt = 0
    else:
        if parser.parse_args().count:
            port_cnt = parser.parse_args().count
        else:
            port_cnt = 65535

    print(f"host_ip {host_ip}")
    print(f"port_cnt {port_cnt}")
    print(f"port {port}")
    
    if port_cnt == 0:
        scan_port(host_ip, port)
    else:
        for p in range(1, port_cnt+1):
            # sock= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # sock.settimeout(0.05)
            # print(f"scan tcp/{p}")
            # scan_port(host_ip, p)
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
