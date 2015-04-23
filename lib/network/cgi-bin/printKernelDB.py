#!/usr/bin/env python
import time
import sqlite3
import cgi
import json

form = cgi.FieldStorage()
name = form.getvalue('name')
conn = sqlite3.connect('system.db')
db = conn.execute("select * from job_list ")
for row in db:
	print row