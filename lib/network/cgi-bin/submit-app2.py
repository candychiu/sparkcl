#!/usr/bin/env python

print """Content-type: text/html


<head>
<link href="bootstrap-3.3.2-dist/css/bootstrap.min.css" rel="stylesheet">
 <link href="bootstrap-3.3.2-dist/css/dashboard.css" rel="stylesheet">
<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
<script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
    <script type="text/javascript">
        function Init () {
            var textarea = document.getElementById ("comments");

            if (textarea.addEventListener) {    // all browsers except IE before version 9
                textarea.addEventListener ("input", OnInput, false);
            }

            if (textarea.attachEvent) { // Internet Explorer and Opera
                textarea.attachEvent ("onpropertychange", OnPropChanged);   // Internet Explorer
            }
        }

            // Firefox, Google Chrome, Opera, Safari from version 5, Internet Explorer from version 9
        function OnInput (event) {
            //alert ("The new content: " + event.target.value);
            var numForm = 0;
            var content = event.target.value;
            $.ajax({
                url: '/myre.py',
                type: 'POST',
                dataType: 'json',
                data:{
                    content: $('#comments').val()
                },
                success: function(data){
                    $("#argForm").empty();

                    for(i=0;i<data;i++){
                        $("#argForm").append('<div id="argForm" class="form-group"> \
                        <label for="arg'+i+'" class="col-sm-2 control-label">Argument '+(i+1)+'</label><div class="col-sm-10"> \
                        <input type="text"  class="form-control" id="arg'+i+'" name="arg'+i+'"/></div></div> \');
                    }

                    $("#argForm").append("<input type='hidden' name='numarg' value="+data+" />");

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
                <li><a href="index.py">Overview <span class="sr-only">(current)</span></a></li>
                <li class="active"><a href="#">Submit Application</a></li>
                <li><a href="#">Slaves</a></li>
                <li><a href="#">Setting</a></li>
              </ul>


    </div>

    <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">

    <h1 class="page-header">Submit Application</h1>
    <form method="post" action="submit-kernel2.py"  class="form-horizontal" enctype="multipart/form-data">
        <div class="form-group">
            <label for="Pname" class="col-sm-2 control-label">Application name </label>
            <div class="col-sm-10">
                <input type="text" class="form-control" id="Pname" name="Pname">
            </div>
        </div>

        <div class="form-group">
            <label for="comments" class="col-sm-2 control-label">Kernel code</label>
            <div class="col-sm-10">
                <textarea name="comments" id="comments"  style="min-width:100%; max-width:100%;" rows="5"></textarea>
            </div>
        </div>
        <div id="argForm">

        </div>

        <div class="form-group">
                <label for="workitem" class="col-sm-2 control-label">Global work item</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="workitem" name="workitem" placeholder="ex. (1,) or (4,5)">
                </div>
        </div>

        <div class="form-group">
                <label for="resultsize" class="col-sm-2 control-label">Result array size</label>
                <div class="col-sm-10">
                    <input type="text" class="form-control" id="resultsize" name="resultsize"  placeholder="ex. (1,) , (4,5) or (1,2,3)">
                </div>
        </div>

        <div class="form-group">
                <label for="data" class="col-sm-2 control-label">Data</label>
                <div class="col-sm-10">
                    <input type="file" name="file">
                </div>
        </div>



    <div class="form-group">
        <div class="col-sm-offset-2 col-sm-10">
            <button type="submit" class="btn btn-default">Submit</button>
            </div>
    </div>
    </form>
    </div>

    </div>
    </div>


</body>
"""
