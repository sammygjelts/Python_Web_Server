# Python_Web_Server
Simple web server for CSCI 356

TESTING INSTRUCTIONS

- Open two terminal windows
- On one, run the command 'radius$: python webserver.py 8085 ./web_files'
    - need a folder called web files, and run whatever port number over 8000 you want
- While that one is waiting for a connection, run 'radius$: telnet radius.holycross.edu 8085'
- Then type 'radius$: GET /hello HTTP/1.1 something'
- You should see your message from the /hello response!
