import errno
import socket

def main():

    serverPort = 13500
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind(('',serverPort))
    serverSocket.setblocking(0)
    print('DNS server is ready ...\n press\'Ctrl + C\' to exit')
    
    try:
        while True:
            try:
                recvHostname, clientAddr = serverSocket.recvfrom(4096)
                results = query_IP_Cname(recvHostname.decode())
                serverSocket.sendto(results.encode(), clientAddr)
            except socket.error as e:
                err = e.args[0]
                if err==errno.EAGAIN or err==errno.EWOULDBLOCK:
                    continue
                else:
                    print(e)
                    
    except KeyboardInterrupt:
        print("DNS server is shutting down ...")
        
    serverSocket.close()
    print("DNS server socket closed")
        

def query_IP_Cname(hostname: str):
    results = '\n'
    try:
        addrInfo = socket.getaddrinfo(hostname, None, 0, 0, 0, socket.AI_CANONNAME)
        for x in addrInfo:
            if x[3] != '':
                #print('CNAME: ',end='')
                #print(x[3])
                results+='CNAME: '
                results+=x[3]
                results+='\n'
            #print('A record: ',end='')
            #print(x[4][0])
            results+='A record: '
            results+=x[4][0]
            results+='\n'
        return results
    except:
        results='Hostname not found.'
        return results
        


if __name__ == '__main__':
    main()


