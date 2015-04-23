#!/usr/bin/env python
import socket
import sys
import time
import sqlite3
import subprocess
import cgi


print """Content-type: text/html


"""

form = cgi.FieldStorage()
slave_ip = form.getvalue('S_IP')
slave_port = form.getvalue('PORT').strip()




HOST, PORT = slave_ip, int(slave_port)
data = "get_slave_info"

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data)

    # Receive data from the server and shut down
    received = sock.recv(1024)
except Exception as e:
    print e
    raise
finally:
    sock.close()

if received.strip():
    print received
else :
    print "0"
