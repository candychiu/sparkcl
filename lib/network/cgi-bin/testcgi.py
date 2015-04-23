#!/usr/bin/env python
import os
import cgi
import sqlite3
import urllib2



form = cgi.FieldStorage()
hostname = form.getvalue('hostname')
platform_name = form.getvalue('platform_name')
device_name = form.getvalue('device_name')
address = form.getvalue('address')
app_id = form.getvalue('app_id')
platform_num = form.getvalue('platform_num')
device_num = form.getvalue('device_num')

print """Content-type: text/html

<html>
<head>
<title>Spark-OpenCL</title>
<link href="bootstrap-3.3.2-dist/css/bootstrap.min.css" rel="stylesheet">
 <link href="bootstrap-3.3.2-dist/css/dashboard.css" rel="stylesheet">

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
            <li  class="active"><a href="index.py">Overview <span class="sr-only">(current)</span></a></li>
            <li ><a href="add-kernel-list.py">Kernel Manager</a></li>
            <li><a href="slaves.py">Slaves Manager</a></li>
             <li><a href="submit-chain-app.py">Submit Application</a></li>
              <li><a href="master-log.py">Logs</a></li>
            <li><a href="setting.py">Setting</a></li>
          </ul>


</div>
<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
<h2> Log </h2><br>"""

print """
<b>Host name:</b> %s<br>
<b>Address:</b> %s<br>
<b>Platform name:</b> %s<br>
<b>Device name:</b> %s<br>
<b>Application id:</b> %s<br>"""%(hostname,address,platform_name,device_name,app_id)

print "<br><b>Log messages</b><br><textarea readonly style='border-radius: 0.4em;border:1px solid Silver  ; background:white; padding-left:10px; padding-top:10px;  width:100%; height:50% ;resize:vertical;' >"
print urllib2.urlopen('http://%s:9091/slaves-cgi/viewlog.py?platform=%s&device=%s&app_id=%s'%(address,platform_num,device_num,app_id)).read().replace('<br>','\n')
print "</textarea>"
print """
</div>
</div>
</div>
</body>
</html>
"""
