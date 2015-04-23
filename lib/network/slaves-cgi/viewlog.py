#!/usr/bin/env python
import os
import cgi
import cgitb; cgitb.enable()
print """Content-type: text/html
"""

form = cgi.FieldStorage()
device = form.getvalue('device')
platform = form.getvalue('platform')
app_id = form.getvalue('app_id')

try :
	print open(os.environ["SPARKCL_HOME"]+"/work/log/slaves/%s_%s/%s.txt"%(platform,device,app_id),"r").read().replace('\n','<br>')
except Exception as e :
	print "log file not found."
