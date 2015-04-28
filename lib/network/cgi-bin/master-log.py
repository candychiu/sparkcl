#!/usr/bin/env python
import sqlite3
import cgi
import os
print """Content-type: text/html

<html>
<head>
<title>Spark feat. OpenCL</title>
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
            <li ><a href="index.py">Overview <span class="sr-only">(current)</span></a></li>
            <li><a href="add-kernel-list.py">Kernel Manager</a></li>
            <li><a href="slaves.py">Slaves Manager</a></li>
             <li><a href="submit-chain-app.py">Submit Application</a></li>
              <li class="active"><a href="master-log.py">Logs</a></li>
            <li><a href="setting.py">Setting</a></li>
          </ul>


</div>



<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
<h3>Logs</h3>
<textarea readonly style='border-radius: 0.4em;border:1px solid Silver  ; background:white; padding-left:10px; padding-top:10px;  width:100%; height:50% ;resize:vertical;' >"""
print open(os.environ['SPARKCL_HOME']+'/work/log/master/logs.txt','r').read()
print """
</textarea>
</div>



</div>
</div>
</body>
</html>"""
