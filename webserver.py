# Author     : Alex Voitik
# Date       : Febuary 15th 2017
# Assignment : Project 1 - Python Web Server
# File Name  : webserver.py

# This server currently creates a socket, binds it to
# the parameters given on the command line, listens to
# the same socket on loop. If the request is GET /hello,
# a message is generated, and sent along to the socket
# with the appropriate header. Error checking is used throughout.


# COMPLETION TIMELINE
#
# Currently I have worked on this project for around 4 hours,
# and I plan to accomplish quite a bit this week now that
# I have a better understanding of the project at hand.
#
# I will next implement handling GET /hello[name] requests, and
# I will do so using regular expressions in order to properly process
# the name. -----DONE
#
# I will also process the static case, using the else statement commented
# out in the code below. ----KINDA DONE
#
# I will, after the things above have been completed, do some extra credit
# on this web server.
#
# I will handle the /index.html requests (Default URL) ----DONE
#
# I would also like to try and handle concurrency, using the knowledge
# I gained in your Operating Systems course
#
# If time is not a factor, I would also like to attemp the POST mini-twitter,
# but we shall see if I get to that.

import socket
import sys
import time
import re

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
        sys.exit(1)
        
    #print parse
    
    # Split the header line, ignoring carraige returns
    method, path, version, other = parse.split(None, 3)
    
    print 'Request path is: ' + path
    
    #If the path is the /hello?[name] case, grab the name and
    # assign m to be true using regular expressions
    # If this is not the case, m will be false
    m = re.search('/hello\?([A-Za-z]*)', path)
    
    if method == 'GET':
        
        if path == '/hello':
            
            # using the time module to get the properly formatted time
            currTime = time.asctime(time.localtime(time.time()))
            message = 'Howdy! How are you today? Today is ' + currTime + '\r\n'
            
            # Send the header along with the message compiled above.
            conn.sendall( 'HTTP/1.1 200 OK\r\n' + 'Date: ' + currTime + '\r\n' +
                         'Server : VoitikWebServer (ajvoit17)\r\n' + 'Content-Length: ' + str(len(message)) + '\r\n'
                         + 'Connection: close\r\n' + 'Content-Type: text/plain\r\n' + message)
            
            print 'Sent response, content length was ' + str(len(message)) + ' bytes'
            
            conn.close()
            
            print 'Closed connection'
    
        # Process /name? case
        elif m:
            
            currTime = time.asctime(time.localtime(time.time()))
            message = 'Howdy ' + m.group(1) +  '! How are you? Today is ' + currTime + '\r\n'
            
            conn.sendall( 'HTTP/1.1 200 OK\r\n' + 'Date: ' + currTime + '\r\n' +
                         'Server : VoitikWebServer (ajvoit17)\r\n' + 'Content-Length: ' + str(len(message)) + '\r\n'
                         + 'Connection: close\r\n' + 'Content-Type: text/plain\r\n' + message)
            
            print 'Sent response, content length was ' + str(len(message)) + ' bytes'
            
            conn.close()
            
            print 'Closed connection'
            
        # Process the static case   
            
        else:
            
            #Change default path to be index.html
            if path == '/':
                path = '/index.html'
                
            try:
                print 'Opening ' + direct + path
                file = open(direct + path, 'r')
                
            except Exception as e:
                
                #If the file cannot be found
                print 'File Not Found'
                conn.send('HTTP/1.1 404')
                sys.exit(1)
            
            data = file.read()
            currTime = time.asctime(time.localtime(time.time()))
            
            # determine the proper type of file extension
            file_extend = set_file_extension(path) 

            # if the file type
            if typecont == -1:
                print 'Error: Bad Request\n'
                conn.send('HTTP/1.1 400')
                sys.exit(1)

            cont_type = 'Content-Type: '+ file_extend +'\r\n\r\n'
            ok_str = 'HTTP/1.1 200 OK\r\n' 
            date = 'Date: ' + currTime +'\r\n'
            server = 'Server: ajvoit17\r\n' 
            content_len ='Content-Length: '+ str(len(data)) +'\r\n'
            connection = 'Connection: close\r\n'
            
            
            message = ok_str + date + server + content_len + connection + cont_type

            print 'Message : ' + message
            conn.sendall(message)
            conn.sendall(data + '\r\n')
            print 'Data Sent'
            
            conn.close()
            
#set_file_extension will take a path, then return the proper file
# type, according to what the path is named. If none are found,
# a -1 is returned.

def set_file_extension(path):

    # grab the end of the path
    extension = path[-4:]
    
    #change extension to lowercase
    extension = ext.lower()
    
    if extension == 'jpeg' or ext == '.jpg':
        file_extend = 'image/jpeg'
    elif extension == 'html':
        file_extend = 'text/html'
    elif extension == '.txt':
        file_extend = 'text/plain'
    elif extension == '.css':
        file_extend = 'text/css'
    elif extension == '.gif':
        file_extend = 'image/gif'
    elif extension == '.png':
        file_extend = 'image/png'
    else:
        
        # Need to check for 2 letter path now
        extension = file_path[-2:]
        if extension == 'js':
            file_extend = 'application/javascript'
        else:
           return -1
        
    print 'Type returned: '+ file_extend 
    
    return file_extend


if __name__ == '__main__':
    main()

    
