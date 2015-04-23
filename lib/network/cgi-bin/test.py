#!/usr/bin/env python
import sqlite3
import subprocess
import sys
import os
from datetime import datetime,time

try:
    arg1 = os.environ["SPARKCL_HOME"]+"/bin/sparkcl-submit.sh"

    proc = subprocess.Popen([arg1], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()


    conn = sqlite3.connect('system.db')
    conn.execute("update job set isComplete=1,finish_time='%s' where id = %s" %(datetime.now().replace(microsecond=0),sys.argv[1]))
    conn.commit()
    conn.close()

    f = open('output_file/%s'%sys.argv[1],'w')
    f.write(out)
    f.close()
except Exception as excp:
    f = open('output_file/err%s'%sys.argv[1],'w')
    f.write(excp)
    f.close()
