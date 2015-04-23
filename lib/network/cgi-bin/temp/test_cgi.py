#!/usr/bin/env python
import subprocess

spark_home = "/home/job/spark-1.2.0/"
arg1 = spark_home+"bin/spark-submit"
arg2 = "/home/job/Desktop/"+"code.py"
arg3 = spark_home+"README.md"
print "Content-type: text/html"
print
print "<title>Test CGI</title>"
print "<p>Hello World!</p>"
proc = subprocess.Popen([arg1+" "+arg2+" "+arg3], stdout=subprocess.PIPE, shell=True)
print "test"
(out, err) = proc.communicate()

print "program output:<br />", out.replace("\n","<br />")
