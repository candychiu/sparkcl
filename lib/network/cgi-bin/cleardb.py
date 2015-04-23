#!/usr/bin/env python
import sqlite3
import subprocess
import sys
import os

#APP_ID = sys.argv[1]

conn = sqlite3.connect('system.db')
conn.execute("DELETE FROM job")
conn.commit()
conn.close()
