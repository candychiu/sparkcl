#!/usr/bin/env python
import sqlite3
import subprocess
import sys
import os
from datetime import datetime, date


conn = sqlite3.connect(os.environ['SPARKCL_HOME']+'/lib/network/cgi-bin/system.db')
conn.execute("insert into job (name,submit_time,isComplete) values(?,?,0)",(sys.argv[1],datetime.now().replace(microsecond=0)))
maxID_t = conn.execute("select max(id) from job")

for row in maxID_t:
    maxID, = row
conn.commit()
conn.close()
print maxID

