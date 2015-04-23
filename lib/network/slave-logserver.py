#!/usr/bin/env python
import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable()  ## This line enables CGI error reporting
import os
import subprocess
import os.path
import sys

print "1"
print os.path.abspath(os.path.join("/home/job/spark-1.2.0/sparkcl/lib/network/slaves-cgi/"))
IP = sys.argv[1]
PORT = 9091
server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = (IP, PORT)
handler.cgi_directories = ["/slaves-cgi"]

httpd = server(server_address, handler)
httpd.serve_forever()