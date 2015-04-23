import SocketServer
import threading
import pyopencl as cl
import re
import json
import sys
import os
sys.path.insert(0, os.environ['SPARKCL_HOME']+'/lib/network/cgi-bin/')
import SlaveDatabase
client_addr= ""

class MyTCPHandler(SocketServer.BaseRequestHandler):

    def __init__(self, request, client_address, server):
        self.sdb = SlaveDatabase.SlaveDatabase()
        self.client_address = client_address
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        return
    def setup(self):
        self.sdb.writeSlaveDB(self.client_address[0],str(7000))
        print self.sdb.getSlaveData()
        print self.client_address
        return SocketServer.BaseRequestHandler.setup(self)
    def handle(self):
        self.data = self.request.recv(1024).strip()
        self.request.sendall(self.data)
    def finish(self):
        self.sdb.deleteSlave(self.client_address[0],str(7000))
        self.sdb.close()
        print self.client_address
        return SocketServer.BaseRequestHandler.finish(self)


class SparkCLMasterServer(SocketServer.ThreadingMixIn,SocketServer.TCPServer):
    pass
    '''
    client_addr=""

    def __init__(self, server_address, handler_class=MyTCPHandler):
        #self.sdb = SlaveDatabase.SlaveDatabase()
        #self.sdb.createSlaveDB()
        print "Connect DB"
        SocketServer.TCPServer.__init__(self, server_address, handler_class)
        return

    def process_request(self, request, client_address):
        sys.stdout.write("Slave connect: ")
        print client_address
        global client_addr
        client_addr = client_address
        print client_address
        #self.sdb.writeSlaveDB(client_address[0],str(7000))
        #print self.sdb.getSlaveData()
        return SocketServer.TCPServer.process_request(self, request, client_address)

    def finish_request(self, request, client_address):
        #self.logger.debug('finish_request(%s, %s)', request, client_address)
        #sys.stdout.write("Finish request: ")
        #print client_address
        return SocketServer.TCPServer.finish_request(self, request, client_address)

    def close_request(self, request_address):

        #self.sdb.deleteSlave(client_addr[0],str(7000))
        sys.stdout.write("Slave disconnect: ")
        print client_addr
        return SocketServer.TCPServer.close_request(self, request_address)
    '''


if __name__ == "__main__" :

    HOST = sys.argv[1]
    PORT = 9000
    try :
        SlaveDatabase.SlaveDatabase().clearSlaveDB()
        server = SparkCLMasterServer((HOST, PORT), MyTCPHandler)
        print "SparkCL Master is running"
        print HOST+":"+str(PORT)
        #server.serve_forever()

        t = threading.Thread(target=server.serve_forever)
        t.daemon = True # don't hang on exit
        t.start()
        while True :
            pass
        #data = raw_input("")
    except KeyboardInterrupt:
        pass
    except Exception as e :
        print e
    finally :
        try :
            server.shutdown()
            server.socket.close()
        except :
            raise
        sys.exit()
        print "\nEnd."
