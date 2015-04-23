#!/usr/bin/env python
import cgi

form = cgi.FieldStorage()
code = form.getvalue('code')

print """Content-type: text/html

"""
print code
