#!/usr/bin/env python
import cgi

form = cgi.FieldStorage()
file = form.getvalue('file')

fileContent = open("output_file/"+file,'r')
print """Content-type: text/html

<html>
<head>
<link href="bootstrap-3.3.2-dist/css/bootstrap.min.css" rel="stylesheet">
<title>Spark-OpenCL</title>
</head>
<body>
<br>
<br>
<div class="row">
<div class="col-md-10 col-md-offset-1" >
<pre style="white-space: pre-wrap;">
<p >
%s
</p>
</pre>
</div>
</div>
<div class="row">
  <p class="text-center"><a href="index.py">Back</a></p>
</div>
</body>
</html>"""%fileContent.read().replace("\n","<br />")
