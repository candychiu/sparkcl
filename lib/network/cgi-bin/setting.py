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
<h3 class="page-header">Setting</h3>
"""


print """
<h4><b>Application Database</b></h4>
<form method="post" action="del-db.py"  class="form-horizontal" enctype="multipart/form-data">
    <div class="form-group">
        <div class="col-sm-10">
            <button type="submit" class="btn btn-default">Clear Database</button>
        </div>
    </div>
</form>
<hr>
<h4><b>Kernel Database</b></h4>
<form method="post" action="del-ke.py"  class="form-horizontal" enctype="multipart/form-data">
    <div class="form-group">
        <div class="col-sm-10">
            <button type="submit" class="btn btn-default">Clear Kernel</button>
        </div>
    </div>
</form>
<hr>
</div>
</div>
</body>
</html>"""
