#!/usr/bin/env python
import time
import sqlite3
import subprocess
import cgi
from datetime import datetime, date


form = cgi.FieldStorage()
val1 = form.getvalue('comments')
Pname = form.getvalue('Pname')
numArg = int(form.getvalue('numarg'))
arg = []

for i in range(numArg):
    arg.append(form.getvalue('arg%s'%i))

conn = sqlite3.connect('system.db')
conn.execute("insert into job (name,submit_time,isComplete) values(?,?,0)",(Pname,datetime.now().replace(microsecond=0)))
maxID_t = conn.execute("select max(id) from job")
for row in maxID_t:
    maxID, = row

code_file = open("kernel_file/%s.py"%maxID,"w")
code_file.write(val1)
code_file.close()
subprocess.Popen(["chmod +x kernel_file/%s.py"%maxID], stdout=subprocess.PIPE, shell=True)

#subprocess.Popen(["nohup ./aaa.sh %s &" %maxID], stdout=subprocess.PIPE, shell=True)
getNohupID = subprocess.Popen(["nohup ./aaa.sh %s > /dev/null 2>&1 & echo $!" %maxID], stdout=subprocess.PIPE, shell=True)
(nohupID, err) = getNohupID.communicate()
nohupID = int(nohupID.strip('\n'))

conn.execute("update job set pid=%s where id=%s"%(nohupID,maxID))
conn.commit()
conn.close()

print """Content-type: text/html

<html>
<head>
<meta http-equiv="refresh" content="0; url=/main.py" />
</head>
<body>
</body>
</html>"""
