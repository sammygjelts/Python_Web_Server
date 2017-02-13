# Author     : Alex Voitik
# Date       : Febuary 13th 2017
# Assignment : Project 1 - Python Web Server
# File Name  : webserver.py

import socket
import sys
import time

def main():
    
    # Check if command line args are valid
    if len(sys.argv) != 3:
        print 'Invalid command line arguments'
        sys.exit(1)
    
    print 'ajvoit17 server running'
    
    portno = int(sys.argv[1])
    direct = sys.argv[2]
    
    try:
        # Create a IPv4 socket (TCP)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
        #bind socket to the port
        s.bind(('', portno))
        print 'Document root is: ' + direct
        print 'Listening on port ', int(portno)
    
        # Max queue of 5
        s.listen(5)
    
    # Error checking
    except socket.error, msg:
        print 'Failed. Error code: ' + str(msg[0]) + ' : ' + msg[1]
        sys.exit(1);

    while 1:
        print 'Waiting for connections.'
        
        # Accept the connection
        conn, addr = s.accept()
        print 'Connected with '  + addr[0] + ':' + str(addr[1])
        
        read_socket(conn, direct)


def read_socket(conn, direct):
    
    try:
        # Recieve data from the socket
        parse = conn.recv(4096)
    except Exception as e:
        print 'Oops, an error happened: ', e
        
    print parse
    
    # Split the header line, ignoring carraige returns
    method, path, version, other = parse.split(None, 3)
    
    print 'Request path is: ' + path
    
    if method == 'GET':
        
        if path == '/hello':
            
            currTime = time.asctime(time.localtime(time.time()))
            message = 'Howdy! How are you today? Today is ' + currTime + '\r\n'
            
            conn.sendall( 'HTTP/1.1 200 OK\r\n' + 'Date: ' + currTime + '\r\n' +
                         'Server : VoitikWebServer (ajvoit17)\r\n' + 'Content-Length: ' + str(len(message)) + '\r\n'
                         + 'Connection: close\r\n' + 'Content-Type: text/plain\r\n' + message)
            
            print 'Sent response, content length was ' + str(len(message)) + ' bytes'
            
            conn.close()
            
            print 'Closed connection'
            
            
            
if __name__ == '__main__':
    main()

    
