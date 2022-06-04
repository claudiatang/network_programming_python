import socket as skt

def main():

    serverPort = 13500
    serverSocket = skt.socket(skt.AF_INET, skt.SOCK_DGRAM)

    serverSocket.bind(('',serverPort))
    print('DNS server is ready ...')
    
    try:
        while True:
            recvHostname, clientAddr = serverSocket.recvfrom(4096)
            print("recvHostname, clientAddr = serverSocket.recvfrom(4096)")
            results = query_IP_Cname(recvHostname.decode())
            print("results = query_IP_Cname(recvHostname.decode())")
            serverSocket.sendto(results.encode(), clientAddr)
            print("serverSocket.sendto(results.encode(), clientAddr)")
    except KeyboardInterrupt:
        print("DNS server is shutting down ...")
        
    serverSocket.close()
    print("DNS server socket closed")
        

def query_IP_Cname(hostname: str):
    results = '\n'
    try:
        addrInfo = skt.getaddrinfo(hostname, None, 0, 0, 0, skt.AI_CANONNAME)
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


