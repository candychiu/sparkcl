
import sqlite3
conn = sqlite3.connect('system.db')
conn.execute('''DROP TABLE IF EXISTS JOB''')
conn.commit()
conn.execute('''CREATE TABLE IF NOT EXISTS JOB
(ID INTEGER primary key AUTOINCREMENT,
name char(20) not null,
submit_time timestamp not null,
finish_time timestamp,
pid INTEGER,
isComplete boolean not null);''')
conn.commit()
conn.close()
