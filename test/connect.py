import subprocess
import re
import socket
import sys

s = socket.socket()
host = sys.argv[1]
port = 9000

s.connect((host, port))

key = raw_input("")

s.close()
