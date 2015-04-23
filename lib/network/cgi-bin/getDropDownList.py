#!/usr/bin/env python
import sqlite3

conn = sqlite3.connect('system.db')
db = conn.execute("select * from JOB_LIST")
select = ""
for row in db:
    select = select + """<option value="%s">%s</option>"""%(row[1],row[1])
print """Content-type: text/html

"""
print "<option value='' selected='selected'>select</option>"+select
