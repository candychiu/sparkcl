#!/usr/bin/env python
import time
import sqlite3
import subprocess
import cgi
import os
from datetime import datetime, date
import cgitb; cgitb.enable()
from xml.etree.ElementTree import Element, SubElement, Comment, tostring


print """Content-type: text/html

"""

form = cgi.FieldStorage()
kernel_code = form.getvalue('comments')
Pname = form.getvalue('Pname')
#workitem = form.getvalue('workitem')
#resultsize = form.getvalue('resultsize')
#ktype = form.getvalue('type')
# numArg = int(form.getvalue('numarg'))
# arg = ""
#
# for i in range(numArg):
#     arg = arg + form.getvalue('arg%s'%i)+" "

print kernel_code
print Pname
conn = sqlite3.connect('system.db')
conn.execute("insert into JOB_LIST (name) values('%s')"%Pname)
maxID_t = conn.execute("select max(id) from JOB_LIST")
for row in maxID_t:
    maxID, = row

kernel_file = open("kernelList_file/%s"%maxID,"w")
kernel_file.write(kernel_code)
kernel_file.close()

# xml_kernel = Element('kernel')
# output_dim = SubElement(xml_kernel,'output_dim')
# output_dim.text = resultsize.strip('(').strip(')').strip(',')
# arguments = SubElement(xml_kernel,'arguments')
# arguments.text = arg.strip(' ').replace(' ',',')
# local_work_size = SubElement(xml_kernel,'local_work_size')
# global_work_size = SubElement(xml_kernel,'global_work_size')
# global_work_size.text = workitem.strip('(').strip(')').strip(',')
# xmlktype = SubElement(xml_kernel,'type')
# xmlktype.text = ktype
# xml_file = open("kernelList_file/%s.xml"%maxID,"w")
# xml_file.write(tostring(xml_kernel))
# xml_file.close()

conn.commit()
conn.close()


print """<html>
<head>
<meta http-equiv="refresh" content="0; url=/show-kernel-list.py" />
</head>
<body>
</body>
</html>"""
