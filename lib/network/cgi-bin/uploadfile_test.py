#!/usr/bin/env python

print """Content-type: text/html

"""

print """<!DOCTYPE html>
<html>
<body>

<form action="cotest.py">
  <input type="file" name="code" accept="file_extension|.py/*">
  <input type="submit">
</form>

<p><strong>Note:</strong> The accept attribute of the input tag is not supported in Internet Explorer 9 (and earlier versions), and Safari 5 (and earlier).</p>
<p><strong>Note:</strong> Because of security issues, this example will not allow you to upload files.</p>

</body>
</html>
"""
