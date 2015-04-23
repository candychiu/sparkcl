import sqlite3
import sys
import os 
from datetime import datetime, date

conn = sqlite3.connect(os.environ['SPARKCL_HOME']+'/lib/network/cgi-bin/system.db')
conn.execute("update job set isComplete=1,finish_time='%s' where id = %s" %(datetime.now().replace(microsecond=0),sys.argv[1]))
conn.commit()
conn.close()