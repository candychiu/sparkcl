#!/usr/bin/env python
import sqlite3
import cgi
conn = sqlite3.connect('system.db')
db = conn.execute("select * from job_list")
print """Content-type: text/html


<head>
<script src="https://google-code-prettify.googlecode.com/svn/loader/run_prettify.js"></script>
<link href="bootstrap-3.3.2-dist/css/bootstrap.min.css" rel="stylesheet">
 <link href="bootstrap-3.3.2-dist/css/dashboard.css" rel="stylesheet">
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
<script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
    <script type="text/javascript">
        function Init () {
            var textarea = document.getElementById ("comments");
            var appName = document.getElementById("namecheck");

            if (textarea.addEventListener) {    // all browsers except IE before version 9
                textarea.addEventListener ("input", OnInput, false);
            }

            if(appName.addEventListener){
                appName.addEventListener("input",checkAppName,false);
            }

            if (textarea.attachEvent) { // Internet Explorer and Opera
                textarea.attachEvent ("onpropertychange", OnPropChanged);   // Internet Explorer
            }
        }

        function removekernel(id){
            //alert(id.value);
            $("#kernel"+id.value).remove();
            $.ajax({
                url: '/remove-kernel.py',
                type: 'POST',
                dataType: 'json',
                data:{
                    kernelid: id.value
                },
                success: function(data){

                }
            });
        }
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

    <h3 class="page-header">Kernel Manager </h3>
"""
for i in db:

    kernelcode = cgi.escape(open("kernelList_file/"+str(i[0]),'r').read(),True)
    print """
    <div class="form-group" id="kernel%s">
        <label for="Pname" class="col-sm-2 control-label">%s</label>
        <div class="col-sm-10" id="namecheck">
            <pre><code class="prettyprint language-c">%s</code></pre>
            <form method="post" action="edit-kernel.py" enctype="multipart/form-data">
                <input type="hidden" name="kid" value="%s">
                <button type="submit" class="btn btn-default"><span class='glyphicon glyphicon-edit' aria-hidden="true"></span></button>
                <button type="button" class="btn btn-default" value="%s" onclick="removekernel(this)"><span class='glyphicon glyphicon-trash' aria-hidden="true"></span></button>
            </form>
        </div>
    </div><div class="col-sm-12"style="height:10px;"></div>"""%(i[0],i[1],kernelcode,i[0],i[0])
# <div class="form-group">
#     <label for="Pname" class="col-sm-2 control-label">Application name </label>
#     <div class="col-sm-10" id="namecheck">
#         <input type="text" class="form-control" id="Pname" name="Pname" autocomplete="off">
#         <div id="avForm">
#
#         </div>
#     </div>
# </div>
print """
<form method="post" action="add-kernel-list.py" enctype="multipart/form-data">
    <button type="submit" class="btn btn-default"><span class='glyphicon glyphicon-plus' aria-hidden="true"></span> Add Kernel</button>
</form>


    </div>

    </div>
    </div>


</body>
"""
