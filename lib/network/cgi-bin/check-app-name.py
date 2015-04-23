#!/usr/bin/env python
import cgi
import sqlite3
print """Content-type: text/html

"""

form = cgi.FieldStorage()
appName = form.getvalue('appName')

conn = sqlite3.connect('system.db')
db = conn.execute("select count(id) from JOB_LIST where name='%s'"%appName)
for count in db:
    pass
print count[0]
