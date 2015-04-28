#!/usr/bin/env python
import socket
import sys
import time
import sqlite3
import subprocess
import cgi
import os 


print """Content-type: text/html


"""

form = cgi.FieldStorage()
slave_ip = form.getvalue('S_IP')
slave_port = form.getvalue('PORT').strip()
slave_id = form.getvalue('S_ID')

print slave_ip
print slave_port
print slave_id
open(os.environ['SPARKCL_HOME']+'/work/log/master/logs.txt','a').write('%s - Starting SLAVE_ID=%s ADDRESS=%s\n'%(time.strftime("%H:%M:%S"),slave_id,slave_ip))
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
    open(os.environ['SPARKCL_HOME']+'/work/log/master/logs.txt','a').write('%s - Starting SLAVE_ID=%s ADDRESS=%s [SUCCESS]\n'%(time.strftime("%H:%M:%S"),slave_id,slave_ip))
else :
    print "0"
    open(os.environ['SPARKCL_HOME']+'/work/log/master/logs.txt','a').write('%s - Starting SLAVE_ID=%s ADDRESS=%s [FAILED]\n'%(time.strftime("%H:%M:%S"),slave_id,slave_ip))
