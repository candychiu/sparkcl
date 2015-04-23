#!/usr/bin/env python
import cgi
import sqlite3

form = cgi.FieldStorage()
name = form.getvalue('Pname')
newCode = form.getvalue('comments')
conn = sqlite3.connect('system.db')
db = conn.execute("select id from job_list where name='%s'"%(name))
for row in db:
    pass
conn.commit()
conn.close()
open("kernelList_file/"+str(row[0]),'w').write(newCode)
print """Content-type: text/html

"""
print """<html>
<head>
<meta http-equiv="refresh" content="0; url=/show-kernel-list.py" />
</head>
<body>
</body>
</html>"""
