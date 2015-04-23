#!/usr/bin/env python
import time
import sqlite3
import subprocess
import cgi
import os
from datetime import datetime, date
import cgitb; cgitb.enable()



def fbuffer(f, chunk_size=10000):
   while True:
      chunk = f.read(chunk_size)
      if not chunk: break
      yield chunk



print """Content-type: text/html

"""


form = cgi.FieldStorage()
kernel_code = form.getvalue('comments')
Pname = form.getvalue('Pname')
numArg = int(form.getvalue('numarg'))
dataset = form.getvalue('data')
arg = ""

for i in range(numArg):
    arg = arg + form.getvalue('arg%s'%i)+" "

print arg
print dataset
print "TEST!"


kernel_file = open("../../../work/temp/kernel.cl","w");
kernel_file.write(kernel_code)
kernel_file.close()

map_argv_file = open("../../../work/temp/map_argv.txt","w");
map_argv_file.write(arg)
map_argv_file.close()

work_item_file = open("../../../work/temp/work_item.txt","w");
work_item_file.write(form.getvalue('workitem'))
work_item_file.close()

result_size_file = open("../../../work/temp/result_size.txt","w");
result_size_file.write(form.getvalue('resultsize'))
result_size_file.close()



fileitem = form['file']

# Test if the file was uploaded
if fileitem.filename:

   # strip leading path from file name to avoid directory traversal attacks
   fn = os.path.basename(fileitem.filename)
   f = open('../../../work/temp/data.txt', 'wb', 10000)

   # Read the file in chunks
   for chunk in fbuffer(fileitem.file):
      f.write(chunk)
   f.close()
   message = '1'

else:
   message = '0'

print message



conn = sqlite3.connect('system.db')
conn.execute("insert into job (name,submit_time,isComplete) values(?,?,0)",(Pname,datetime.now().replace(microsecond=0)))
maxID_t = conn.execute("select max(id) from job")
for row in maxID_t:
    maxID, = row

#maxID = maxID-1 ;
#subprocess.Popen(["nohup ./start-submit.sh %s &" %maxID], stdout=subprocess.PIPE, shell=True)
getNohupID = subprocess.Popen(["nohup %s %s > /dev/null 2>&1 & echo $!" %(os.environ["SPARKCL_HOME"]+"/bin/sparkcl-submit.sh",maxID)], stdout=subprocess.PIPE, shell=True)
(nohupID, err) = getNohupID.communicate()
nohupID = int(nohupID.strip('\n'))

save_kernel = open("kernel_file/"+str(maxID),"w");
save_kernel.write(kernel_code)
save_kernel.close()

conn.execute("update job set pid=%s where id=%s"%(nohupID,maxID))
conn.commit()
conn.close()

#proc = subprocess.Popen(["/home/job/spark-1.2.0/sparkcl/bin/sparkcl-submit.sh"], stdout=subprocess.PIPE, shell=True)
#(out,err) = proc.communicate()




print """<html>
<head>
<meta http-equiv="refresh" content="0; url=/index.py" />
</head>
<body>
</body>
</html>"""
