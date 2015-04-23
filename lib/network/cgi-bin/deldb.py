import sqlite3

conn = sqlite3.connect('system.db')
conn.execute("drop table job")
conn.commit()
conn.close()

