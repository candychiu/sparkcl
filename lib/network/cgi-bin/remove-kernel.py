#!/usr/bin/env python
import cgi
import sqlite3

form = cgi.FieldStorage()
kernelid = form.getvalue('kernelid')
conn = sqlite3.connect('system.db')
db = conn.execute("delete from job_list where id=?",kernelid)
conn.commit()
conn.close()
print """Content-type: text/html

"""
print "success";
