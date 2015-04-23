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
slave_id = form.getvalue('S_ID')

print slave_ip
print slave_port
print slave_id


HOST, PORT = slave_ip, int(slave_port)
data = "slave_start(%s)" %(slave_id)

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect((HOST, PORT))
    sock.sendall(data + "\n")

    # Receive data from the server and shut down
    received = sock.recv(1024)
except Exception as e:
    print e
    raise
finally:
    sock.close()

if received.strip() == "1" :
    print "1"
else :
    print "0"
