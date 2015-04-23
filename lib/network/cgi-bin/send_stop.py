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
slave_id = form.getvalue('S_ID')

print slave_ip
print slave_id


HOST, PORT = slave_ip, 9001
data = "slave_stop(%s)" %(slave_id)

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, 7000))
    sock.sendall(data + "\n")

    # Receive data from the server and shut down
    received = sock.recv(1024)
finally:
    sock.close()

if received.strip() == "1" :
    print "1"
else :
    print "0"
