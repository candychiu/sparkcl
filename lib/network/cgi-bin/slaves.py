#!/usr/bin/env python
import sqlite3
import socket
import json
from StringIO import StringIO

conn = sqlite3.connect('system.db')
slave = conn.execute("select ip,port from slave")

print """Content-type: text/html

<html>
<head>
<title>Spark feat. OpenCL</title>
<link href="bootstrap-3.3.2-dist/css/bootstrap.min.css" rel="stylesheet">
<link href="bootstrap-3.3.2-dist/css/dashboard.css" rel="stylesheet">
<link href="bootstrap-3.3.2-dist/css/blinker.css" rel="stylesheet">
<script src="bootstrap-3.3.2-dist/js/jquery.min.js"></script>


<script>

$( document ).ready(function() {
console.log( "ready!" );

$( ".start" ).click(function() {
 var id = $(this).children('#hid').val();
 $("#"+id).html("<p class='text-info'><b class='blink_me'>WAIT");
 var ip  = $(this).children('.ip_address').val();
 var device_id = $(this).children('.device_id').val();
 $.get( "send_start.py", { S_IP: ip, PORT: "7000" , S_ID:device_id} )
 .done(function( data ) {
    $("#"+id).html("<p class='text-success'><b>UP");

    });

});



$( ".stop" ).click(function() {
 var id = $(this).children('#hid').val();
 $("#"+id).html("<p class='text-info'><b class='blink_me'>WAIT");
 var ip  = $(this).children('.ip_address').val();
 var device_id = $(this).children('.device_id').val();
 $.get( "send_stop.py", { S_IP:ip, PORT: "7000" , S_ID:device_id} )
 .done(function( data ) {
    $("#"+id).html("<p class='text-danger'><b>DOWN");

    });



});

});


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
            <li class="active"><a href="slaves.py">Slaves Manager</a></li>
            <li ><a href="submit-chain-app.py">Submit Application</a></li>
            <li><a href="master-log.py">Logs</a></li>
            <li><a href="setting.py">Setting</a></li>
        </ul>


</div>



<div class="col-sm-9 col-sm-offset-3 col-md-10 col-md-offset-2 main">
<h3 class="page-header">Slaves</h3>

"""

row_count = 0
for row in slave :
    #print str(row[0]) + ":" + str(row[1]) + "<br>"
    try :
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((row[0], int(row[1])))
        sock.sendall("get_hostname")
        received = sock.recv(1024)
        print "<h4><b>"+received+" "+row[0]+"</b></h4>"
        sock.close()
        print """
            <div class="table-responsive"><table class="table  table-condensed" style="font-size:14px">
            <thead>
            <tr>
            <th>Platform</th>
            <th>Device</th>
            <th>Status</th>
            <th></th>
            </tr>
            </thead>

        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((row[0], int(row[1])))
        sock.sendall("get_slave_info")
        received = sock.recv(1024)
        io = StringIO(received)
        data = json.load(io)
        #print

        for d in range(0,len(data)) :
            #print data[d]
            print "<tr>"
            print "<td>",data[d]["platform_name"],"</td>"
            print "<td>",data[d]["device_name"],"</td>"
            if data[d]["alive"] == "1" :
                is_alive = "<p class='text-success'>UP"
            else :
                is_alive = "<p class='text-danger'>DOWN"
            print "<td id='h"+str(row_count)+"d"+str(d)+"'>",is_alive,"</p></td>"
            print "<td><a class='start'>start<input class='hid' id='hid' type='hidden' value='h"+str(row_count)+"d"+str(d)+"'>\
            <input class='ip_address' type='hidden' value='"+row[0]+"'> \
            <input class='device_id' type='hidden' value='"+str(d)+"'></a>, \
            <a class='stop'>stop<input class='hid' id='hid' type='hidden' value='h"+str(row_count)+"d"+str(d)+"'> \
            <input class='ip_address' type='hidden' value='"+row[0]+"'> \
            <input class='device_id' type='hidden' value='"+str(d)+"'></a> \
            </td>"
            print "</tr>"
        #print received + " " +str(row[0]) +  "<br>"
        sock.close()

        print """

            </table>
            </div>
        """
    except Exception as e:
        print e
    row_count = row_count + 1

print """

</div>



</div>
</div>
</body>
</html>"""
