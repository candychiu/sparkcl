#!/usr/bin/env python
import sqlite3
import subprocess
import sys
import os
from datetime import datetime,time

APP_ID = sys.argv[1]

conn = sqlite3.connect('system.db')
conn.execute("update job set isComplete=1,finish_time='%s' where id = %s" %(datetime.now().replace(microsecond=0),APP_ID))
conn.commit()
conn.close()
