#!/usr/bin/env python
import cgi
import subprocess
import sqlite3

form = cgi.FieldStorage()
aid = form.getvalue('id')
pid = form.getvalue('pid')

#conn = sqlite3.connect('system.db')
#conn.execute("delete from job where id=%s"%aid)

#conn.commit()
#conn.close()



#kill = subprocess.Popen(["kill -SIGTERM "+ str(pid)], stdout=subprocess.PIPE, shell=True)
#kill.communicate()
subprocess.call(["kill", "-SIGTERM",str(pid)])
print "ok"


print """<html>
<head>
<meta http-equiv="refresh" content="0; url=/index.py" />
</head>
<body>
</body>
</html>"""
