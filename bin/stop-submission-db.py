#!/usr/bin/env python
import sqlite3
import subprocess
import sys
import os

APP_ID = sys.argv[1]

conn = sqlite3.connect(os.environ['SPARKCL_HOME']+'/lib/network/cgi-bin/system.db')
conn.execute("update job set isComplete=1 where id = %s" %APP_ID)
conn.commit()
conn.close()
