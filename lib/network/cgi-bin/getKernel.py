#!/usr/bin/env python
import cgi
import os
form = cgi.FieldStorage()
file = form.getvalue('file')


print """Content-type: text/html

<html>
<head>
<link href="bootstrap-3.3.2-dist/css/bootstrap.min.css" rel="stylesheet">
<title>Spark-OpenCL</title>
<script src="https://google-code-prettify.googlecode.com/svn/loader/run_prettify.js"></script>
</head>
<body>
<br>
<br>
<div class="row">
<div class="col-md-10 col-md-offset-1">
"""

file_count = 0
while os.path.isfile("kernel_file/"+file+"/"+str(file_count)) :
	print """<pre>
	<code class="prettyprint language-c">
%s
	</code></pre><br>
	""" % (cgi.escape(open("kernel_file/"+str(file)+"/"+str(file_count),"r").read(),True))
	file_count = file_count + 1

print """
</div>
</div>
<div class="row">
  <p class="text-center"><a href="index.py">Back</a></p>
</div>
</body>
</html>"""
