#!/usr/bin/env python
import time
import sqlite3
import cgi
import json

form = cgi.FieldStorage()
name = form.getvalue('name')
conn = sqlite3.connect('system.db')
db = conn.execute("select * from job_list where name = '%s'"%name)
for row in db:
    pass
code = open('kernelList_file/'+str(row[0]),'r').read()
print """Content-type: text/html

"""
print json.dumps({'id':row[0],'name':row[1],'code':cgi.escape(code,True)})
