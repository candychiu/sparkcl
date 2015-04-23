#!/usr/bin/env python
import sqlite3
#sssss
conn = sqlite3.connect('system.db')
running = conn.execute("select id,name,submit_time,pid from job where iscomplete=0 ORDER BY id desc")
complete = conn.execute("select id,name,submit_time,finish_time from job where iscomplete is not 0 ORDER BY id desc")
print """Content-type: text/html

<html>
<head>
<title>SparkCL</title>
<link href="bootstrap-3.3.2-dist/css/bootstrap.min.css" rel="stylesheet">
 <link href="bootstrap-3.3.2-dist/css/dashboard.css" rel="stylesheet">
</head>
<body>
<nav class="navbar navbar-inverse navbar-fixed-top" >
      <div class="container-fluid">
        <div class="navbar-header" >
          <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
            <span class="sr-only">Toggle navigation</span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
            <span class="icon-bar"></span>
          </button>
          <a class="navbar-brand" href="#"><small>SPARKCL</small></a>
        </div>
        <div id="navbar" class="navbar-collapse collapse">
          <ul class="nav navbar-nav navbar-right">
            <!--<li><a href="#">Help</a></li>-->
          </ul>
        </div>
      </div>
</nav>


<div class="container-fluid">
<div class="row">
<div class="col-sm-3 col-md-2 sidebar">

          <ul class="nav nav-sidebar">
            <li class="active"><a href="index.py">Overview <span class="sr-only">(current)</span></a></li>
            <li><a href="show-kernel-list.py">Kernel Manager</a></li>
            <li><a href="slaves.py">Slaves Manager</a></li>
             <li><a href="submit-chain-app.py">Submit Application</a></li>
              <li><a href="master-log.py">Logs</a></li>
            <li><a href="setting.py">Setting</a></li>
          </ul>


</div>



<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
<h3>Running Application</h3>
"""
print """<div class="table-responsive"><table class="table table-hover  table-condensed" style="font-size:14px">
<thead>
<tr>
<th>App ID</th>
<th>App name</th>
<th>Submit time</th>
<th>PID</th>
</tr>
</thead>
"""
for row in running:
    print "<tr>"
    print "<td><a href='/showall.py?aid=%s'>%s</a></td>"%(row[0],row[0])
    print "<td>"+str(row[1])+"</td>"
    print "<td>"+str(row[2])+"</td>"
    print """<td><a href="/killprocess.py?pid=%s&id=%s">Kill</a></td>"""%(row[3],row[0])
    print "</tr>"
print """
</table>
</div>


<h3>Complete Application</h3>
"""
print """<div class="table-responsive"><table class="table table-hover  table-condensed" style="font-size:14px">
<thead>
<tr>
<th>App ID</th>
<th>App name</th>
<th>Submit time</th>
<th>Finish time</th>
<th style="text-align:center">Output</th>
<th style="text-align:center">Kernel Code</th>
</tr>
</thead>
"""
for row in complete:
    print "<tr>"
    #print "<td>"+str(row[0])+"</td>"
    print """<td><a href="/showall.py?aid=%s">%s</a></td>"""%(row[0],row[0])
    print "<td>"+str(row[1])+"</td>"
    print "<td>"+str(row[2])+"</td>"
    print "<td>"+str(row[3])+"</td>"
    print """<td align="center"><a href="/getOutputFile.py?file=%s"><span class="glyphicon glyphicon-search"></span></a>&nbsp;&nbsp;<a href="output_file/%s"><span class="glyphicon glyphicon-download-alt"></span></a></td>"""%(row[0],row[0])
    print """<td align="center"><a href="/getKernel.py?file=%s"><span class="glyphicon glyphicon-search"></span></a>&nbsp;&nbsp;<a ><span class="glyphicon glyphicon-download-alt"></span></a></td>"""%row[0]
    print "</tr>"
    #print "     "+str(row[0])+" "+str(row[1])+" "+str(row[2])+ """<a href="/getOutputFile.py?file=%s">Output</a>"""%row[0]+"""    <a href="/getKernel.py?file=%s">Kernel</a>"""%row[0]
print """
</table>
</div>
<form method="post" action="del-db.py"  class="form-horizontal" enctype="multipart/form-data">
    <div class="form-group">
        <div class="col-sm-offset-2 col-sm-10">
            <button type="submit" class="btn btn-default">Clear Database</button>
            </div>
    </div>
</form>
</div>



</div>
</div>
</body>
</html>"""
