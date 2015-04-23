#!/usr/bin/env python
import sqlite3
import cgi
import re
from datetime import datetime,time
import socket
import json
from StringIO import StringIO
form = cgi.FieldStorage()
aid = form.getvalue('aid')

#match = re.compile('KERNEL_CODE=\"\"\"(.*)\"\"\"',re.DOTALL).findall(fileContent)
conn = sqlite3.connect('system.db')
app = conn.execute("select id,name,iscomplete,submit_time,finish_time from job where id=%s"%aid)
for row in app:
    pass

print """Content-type: text/html

<html>
<head>
<title>Spark-OpenCL</title>
<link href="bootstrap-3.3.2-dist/css/bootstrap.min.css" rel="stylesheet">
 <link href="bootstrap-3.3.2-dist/css/dashboard.css" rel="stylesheet">
 <script src="https://google-code-prettify.googlecode.com/svn/loader/run_prettify.js"></script>
</head>
<body>
<nav class="navbar navbar-inverse navbar-fixed-top">
      <div class="container-fluid">
        <div class="navbar-header">
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="index.py">SPARKCL</a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav navbar-right">
            <li><a href="#">Help</a></li>
          </ul>
        </div>
      </div>
</nav>


<div class="container-fluid">
<div class="row">
<div class="col-sm-3 col-md-2 sidebar">

           <ul class="nav nav-sidebar">
            <li class="active" ><a href="index.py">Overview <span class="sr-only">(current)</span></a></li>
            <li ><a href="show-kernel-list.py">Kernel Manager</a></li>
            <li><a href="slaves.py">Slaves Manager</a></li>
             <li><a href="submit-chain-app.py">Submit Application</a></li>
              <li><a href="master-log.py">Logs</a></li>
            <li><a href="setting.py">Setting</a></li>
          </ul>



</div>
<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">"""
print """<h3>Application: %s</h3>"""%row[1]
print "<br>"
if row[2] == 0:
    print "<b>Status</b>: <b><font color='blue'>RUNNING</font></b><br>"
elif row[2] == 1:
    print "<b>Status</b>: <b><font color='green'>COMPLETE</font></b><br>"
elif row[2] == 2:
    print "<b>Status</b>: <b><font color='orange'>CANCEL</font></b><br>"
elif row[2] == 3:
    print "<b>Status</b>: <b><font color='red'>ERROR</font></b><br>"

print """<b>Application ID</b>: %s<br>"""%row[0]
print """<b>Submit time</b>: %s<br>"""%row[3]
print """<b>Finish time</b>: %s<br>"""%row[4]
print """<b>Process time</b>: %s<br>"""%(datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S')-datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S'))

print """<h3>Logs</h3>"""

conn = sqlite3.connect('system.db')
slave = conn.execute("select ip,port from slave")


row_count = 0
slave_data = []
for row in slave :
    #print str(row[0]) + ":" + str(row[1]) + "<br>"
    try :
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((row[0], int(row[1])))
        sock.sendall("get_hostname")
        received = sock.recv(1024)
        hostname = received
        sock.close()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((row[0], int(row[1])))
        sock.sendall("get_slave_info")
        received = sock.recv(1024)
        io = StringIO(received)
        data = json.load(io)
        #print

        for d in range(0,len(data)) :
            #print data[d]
            slave_data.append((hostname,data[d]["platform_name"],data[d]["device_name"],data[d]["alive"],row[0],data[d]["platform_num"],data[d]["device_num"]))

           
        #print received + " " +str(row[0]) +  "<br>"
    except Exception as e:
        print e
    row_count = row_count + 1

#print slave_data

print """
<table class="table table-bordered table-condensed" style="font-size:14px">
  <thead>
  <tr>
    <th>Host name</th>
    <th>Device</th>
    <th>Log</th>
  </tr>
  </thead>
  <tbody>
  """


form_str = """ <form id='form%s' method="POST" action="testcgi.py">
<input type='hidden' name='hostname' value='%s' />
<input type='hidden' name='address' value='%s' />
<input type='hidden' name='platform_name' value='%s' />
<input type='hidden' name='device_name' value='%s' />
<input type='hidden' name='app_id' value='%s' />
<input type='hidden' name='platform_num' value='%s' />
<input type='hidden' name='device_num' value='%s' />
<a onclick="document.getElementById('form%s').submit();" ><span class="glyphicon glyphicon-file" aria-hidden="true"></span></a>
</form>"""

r_count = 0
for r in slave_data :
  print """
    <tr>
    <td>%s</td>
    <td>%s</td>
    <td>%s</td>
    </tr>
  """%(r[0],r[1]+','+r[2],form_str%(r_count,r[0],r[4],r[1],r[2],aid,r[5],r[6],r_count))
  r_count = r_count + 1
print """
  </tbody>
</table>"""

print """
</div>
</div>
</div>
</body>
</html>
"""
