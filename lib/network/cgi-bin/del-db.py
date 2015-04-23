#!/usr/bin/env python
import sqlite3

conn = sqlite3.connect('system.db')
conn.execute("delete from job_list")
conn.execute("delete from job")
conn.execute("delete from slave")
conn.commit()
conn.close()
print """Content-type: text/html

"""
print """<html>
<head>
<meta http-equiv="refresh" content="0; url=/index.py" />
</head>
<body>
</body>
</html>"""
