#!/usr/bin/env python
import sqlite3
import cgi

form = cgi.FieldStorage()
kernelid = form.getvalue('kid')
conn = sqlite3.connect('system.db')
db = conn.execute("select * from job_list where id=?",kernelid)
for row in db:
    pass
print """Content-type: text/html


<head>
<link href="bootstrap-3.3.2-dist/css/bootstrap.min.css" rel="stylesheet">
 <link href="bootstrap-3.3.2-dist/css/dashboard.css" rel="stylesheet">
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
<script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
    <script type="text/javascript">

    </script>
</head>



<body onload="Init ();">

    <nav class="navbar navbar-inverse navbar-fixed-top">
          <div class="container-fluid">
            <div class="navbar-header">
              <button type="button" class="navbar-toggle collapsed" data-toggle="collapse" data-target="#navbar" aria-expanded="false" aria-controls="navbar">
                <span class="sr-only">Toggle navigation</span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
                <span class="icon-bar"></span>
              </button>
              <a class="navbar-brand" href="#">SPARKCL</a>
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
            <li ><a href="index.py">Overview <span class="sr-only">(current)</span></a></li>
            <li class="active"><a href="show-kernel-list.py">Kernel Manager</a></li>
            <li><a href="slaves.py">Slaves Manager</a></li>
             <li><a href="submit-chain-app.py">Submit Application</a></li>
              <li><a href="master-log.py">Logs</a></li>
            <li><a href="setting.py">Setting</a></li>
          </ul>

    </div>

    <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">

    <h3 class="page-header">Edit Kernel</h3>
    <form method="post" action="submit-edit.py"  class="form-horizontal" enctype="multipart/form-data">
        <div class="form-group">
            <label for="Pname" class="col-sm-2 control-label">Application name </label>
            <div class="col-sm-10" id="namecheck">"""
print "         <input type='text' class='form-control' id='Pname' name='Pname' autocomplete='off' value='%s' READONLY>"%(row[1])
print """   </div>
        </div>

        <div class="form-group">
            <label for="comments" class="col-sm-2 control-label">Kernel code</label>
            <div class="col-sm-10">
                <textarea name="comments" id="comments"  style="min-width:100%; max-width:100%;" rows="5">"""

print open("kernelList_file/"+str(kernelid),'r').read()

print        """</textarea>
            </div>
        </div>



    <div class="form-group">
        <div class="col-sm-offset-2 col-sm-10">
            <button type="submit" class="btn btn-default">Edit</button>
        </div>
    </div>
    </form>
    </div>

    </div>
    </div>


</body>"""
