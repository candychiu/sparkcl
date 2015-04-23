#!/usr/bin/env python

print """Content-type: text/html

"""

print """<html><body>
<form enctype="multipart/form-data" action="save_file.py" method="post">
<p>File: <input type="file" name="file"></p>
<p><input type="submit" value="Upload"></p>
</form>
</body></html>
"""
