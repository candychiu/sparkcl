#!/usr/bin/env python
import sqlite3

conn = sqlite3.connect('system.db')
db = conn.execute("select * from JOB_LIST")
select = ""
for row in db:
    select = select + """<option value="%s">%s</option>"""%(row[1],row[1])
print """Content-type: text/html


<head>
<script src="prettify/prettify.js"></script>
 <link href="prettify/prettify.css" rel="stylesheet">



<link href="bootstrap-3.3.2-dist/css/bootstrap.min.css" rel="stylesheet">
 <link href="bootstrap-3.3.2-dist/css/dashboard.css" rel="stylesheet">
 <link href="bootstrap-3.3.2-dist/css/mycss.css" rel="stylesheet">



<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>


<script src="http://code.jquery.com/jquery-1.11.0.min.js"></script>
    <script type="text/javascript">
        var i=0;
        function addMoreKernel(){
            $.get('getDropDownList.py', function(data) {
                i++;
                $("#addDropDownList").append("<hr><div class='kernel"+i+"'>\
                                                <select  class='form-control' id='"+i+"' name='kernel"+i+"' onchange='getDetail(this)'>\
                                                    "+data+"\
                                                    </select><br>\
                                                    <div class='detail"+i+"' id='detailBorder'>\
                                                    </div>\
                                                </div>");
                $(".numkernel").remove();
                $("#addDropDownList").append("<div class='numKernel'><input type='hidden' name='numKernel' value='"+(i+1)+"' /></div>");
            });
        }
        function removeKernel(){
            $(".numkernel").remove();
            $(".kernel"+i).remove();
            i--;
            $("#addDropDownList").append("<div class='numKernel'><input type='hidden' name='numKernel' value='"+(i+1)+"' /></div>");        }
        function getDetail(name){
            var value = name.value;
            var id = name.id;
            $.ajax({
                url: '/getDetail.py',
                type: 'POST',
                dataType: 'json',
                data:{
                    name: value
                },
                success: function(data){

                    //alert(data.id);
                    $(".detail"+id).empty();
                    $(".detail"+id).append("<b>Kernel code </b><br>\
                    <pre  class='prettyprint' style='border-radius: 0px; border: 0px; padding-top: 25px;\
                    padding-bottom: 25px;  padding-left: 25px; font-family: \'Courier New\';'>"+data.code+"</pre>\
                    <br><b>Configuration</b>\
                    <pre style='border-radius: 0px; border: 0px; padding-top: 25px;\
                    padding-bottom: 25px;  padding-left: 25px; font-family: \'Courier New\';'><b>Argument          : </b><input name='argv"+name.id+"' type='text' style = ' width:50%; border: none; border-color: transparent; background: transparent;' placeholder='None'> </input><br>\
<b>Global work item  : </b><input name='global"+name.id+"' type='text' style = 'border: none; border-color: transparent; background: transparent;' placeholder='None'> </input><br>\
<b>Local work item   : </b><input name='local"+name.id+"' type='text' style = 'border: none; border-color: transparent; background: transparent;' placeholder='None'> </input><br>\
<b>Resute size       : </b><input name='result"+name.id+"' type='text' style = 'border: none; border-color: transparent; background: transparent;' placeholder='None'> </input><br>\
<b>Type              : </b><input name='type"+name.id+"' type='text' style = 'border: none; border-color: transparent; background: transparent;' placeholder='map, reduce'> </input><br>\
                    <input type='hidden' name='kernel_id_"+name.id+"' value='"+data.id+"' /></div>\
                    <input type='hidden' name='kernel_type_"+name.id+"' value='"+data.type+"' /></div>\
                    "); 
                    prettyPrint();
                }
            });
        }
    </script>
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
              <a class="navbar-brand" href="#"><small>SPARKCL</small></a>
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
            <li  ><a href="index.py">Overview <span class="sr-only">(current)</span></a></li>
            <li ><a href="show-kernel-list.py">Kernel Manager</a></li>
            <li><a href="slaves.py">Slaves Manager</a></li>
            <li class="active"><a href="submit-chain-app.py">Submit Application</a></li>
            <li><a href="master-log.py">Logs</a></li>
            <li><a href="setting.py">Setting</a></li>
        </ul>


    </div>

    <div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">

    <h3 >Submit Application</h3>
    <hr>
    <form method="post" action="submit-multi-app.py"  class="form-horizontal" enctype="multipart/form-data">

    <div class="form-group">
            <label for="data" class="col-md-1 control-label">Data</label>
            <div class="col-sm-10">
                <input type="file" name="file">
            </div>
    </div>

    <div id="addDropDownList">
        <div class="kernel0">
            <select class='form-control' id="0" name="kernel0" onchange="getDetail(this)">"""
print "<option value='' selected='selected'>select</option>"+select
print """
            </select><br>
            <div class="detail0" id="detailBorder">
            </div>
        </div>
        <div class='numKernel'><input type='hidden' name='numKernel' value='1' /></div>
    </div>
    <br>
     <div class="col-md-4  " >
        <button type="button" class="btn btn-success" onclick="addMoreKernel()">
            <span class="glyphicon glyphicon-plus" aria-hidden="true"></span>
        </button>
        <button type="button" class="btn btn-danger" onclick="removeKernel()">
 <span class="glyphicon glyphicon-minus" aria-hidden="true"></span>
        </button>
    </div>
  
        <div class="col-md-4  col-md-offset-4 " style="text-align: right;">
            <button type="submit" class="btn btn-primary " >Submit</button>
        </div>
   
    </form>
    </div>

    </div>
    </div>





</body>
"""
