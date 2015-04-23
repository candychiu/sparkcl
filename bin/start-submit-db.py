import sqlite3
import os 
from datetime import datetime, date


conn = sqlite3.connect(os.environ['SPARKCL_HOME']+'/lib/network/cgi-bin/system.db')
conn.execute("insert into job (name,submit_time,isComplete) values(?,?,0)",("test_submit",datetime.now().replace(microsecond=0)))
maxID_t = conn.execute("select max(id) from job")

for row in maxID_t:
	maxID, = row

if maxID is None :
	maxID = 1
conn.commit()
conn.close()

print maxID