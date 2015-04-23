#!/usr/bin/env python
import os
import cgi
print """Content-type: text/html

"""

form = cgi.FieldStorage()
app_id = form.getvalue('app_id')
app_id = form.getvalue('platform')
app_id = form.getvalue('app_id')
print app_id
print open(os.environ["SPARKCL_HOME"]+"/work/log/slaves/0_0/%s.txt"%(app_id),"r").read().replace('\n','<br>')