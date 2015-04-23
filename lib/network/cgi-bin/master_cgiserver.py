#!/usr/bin/env python
import BaseHTTPServer
import CGIHTTPServer
import cgitb; cgitb.enable()  ## This line enables CGI error reporting
import sqlite3
import sys

conn = sqlite3.connect('system.db')
conn.execute('''DROP TABLE IF EXISTS SLAVE''')
conn.commit()
conn.execute('''CREATE TABLE IF NOT EXISTS SLAVE
(ID INTEGER primary key AUTOINCREMENT,
ip char(20) not null,
port char(20) not null);''')

conn.execute('''CREATE TABLE IF NOT EXISTS JOB
(ID INTEGER primary key AUTOINCREMENT,
name char(20) not null,
submit_time timestamp not null,
finish_time timestamp,
pid INTEGER,
isComplete boolean not null);''')
conn.commit()

conn.execute('''CREATE TABLE IF NOT EXISTS JOB_LIST
(ID INTEGER primary key AUTOINCREMENT,
name text not null UNIQUE ON CONFLICT IGNORE);''')
conn.commit()
conn.close()

server = BaseHTTPServer.HTTPServer
handler = CGIHTTPServer.CGIHTTPRequestHandler
server_address = (sys.argv[1], int(sys.argv[2]))
handler.cgi_directories = ["/"]

httpd = server(server_address, handler)
httpd.serve_forever()


print "Server Start"
