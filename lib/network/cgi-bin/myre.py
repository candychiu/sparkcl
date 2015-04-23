#!/usr/bin/env python
import re
import cgi
print """Content-type: text/html

"""

form = cgi.FieldStorage()
content = form.getvalue('content')
match = re.compile('__kernel.*\((.*)\){',re.MULTILINE).findall(content)
print len(str(match).split(','))
