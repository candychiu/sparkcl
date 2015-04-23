import sqlite3
import os
class SlaveDatabase:

    def __init__(self) :
        self.SlaveSBPath = os.environ['SPARKCL_HOME']+'/lib/network/cgi-bin/system.db'
        self.conn = sqlite3.connect(self.SlaveSBPath )
    def createSlaveDB(self):

        self.conn.execute('''DROP TABLE IF EXISTS SLAVE''')
        self.conn.commit()
        self.conn.execute('''CREATE TABLE IF NOT EXISTS SLAVE
        (ID INTEGER primary key AUTOINCREMENT,
        ip char(20) not null,
        port char(20) not null);''')
        self.conn.commit()
    #    self.conn.close()
    def writeSlaveDB(self,slave_ip,slave_port):
        #conn = sqlite3.connect(self.SlaveSBPath )
        self.conn.execute("insert into slave (ip,port) values (?,?)",(slave_ip,slave_port))
        self.conn.commit()
    #    self.conn.close()
    def getSlaveData(self):
        slave = []
        #conn = sqlite3.connect(self.SlaveSBPath )
        db = self.conn.execute("select ip,port from slave")
        for i in db:
            myDict = {}
            myDict['ip']=i[0]
            myDict['port']=i[1]
            slave.append(myDict)
        #conn.close()
        return slave
    def deleteSlave(self,slave_ip,slave_port):
        #conn = sqlite3.connect(self.SlaveSBPath )
        print slave_ip
        print slave_port
        self.conn.execute("delete from slave where ip='"+slave_ip+"' and port='"+slave_port+"'")
        self.conn.commit()
        #    conn.close()

    def close(self):
        self.conn.close()

    @staticmethod
    def clearSlaveDB():
        conn = sqlite3.connect(os.environ['SPARKCL_HOME']+'/lib/network/cgi-bin/system.db')
        conn.execute('''DROP TABLE IF EXISTS SLAVE''')
        conn.commit()
        conn.execute('''CREATE TABLE IF NOT EXISTS SLAVE
        (ID INTEGER primary key AUTOINCREMENT,
        ip char(20) not null,
        port char(20) not null);''')
        conn.commit()
