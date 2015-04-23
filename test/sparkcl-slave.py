import SlaveController
import SocketServer
import socket
import pyopencl as cl
import re
import json
import sys
import os

sparkcl_slaves = []
platform_counter = 0
json_data = []
#slave1 = SlaveController.SlaveController()
#slave1.start("192.168.12.14")
master_ip = sys.argv[2]
HOST = sys.argv[1]
class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()

        match1 = re.match( r'^slave_start\((\d+)\)\Z',self.data, re.M|re.I)
        match2 = re.match( r'^slave_stop\((\d+)\)\Z',self.data, re.M|re.I)

        print "From client : " +self.data
        try:
            if self.data == "get_slave_info" :
                print json_data
                self.request.sendall(json_data)
            elif match1 :
                out = sparkcl_slaves[int(match1.group(1))].start(master_ip)
                self.request.sendall(str(out))
            elif match2 :
                sparkcl_slaves[int(match2.group(1))].stop()
                self.request.sendall("1")
            else:
                self.request.sendall("invalid command")
        except Exception as e:
            print "<br>"+e+"<br>"
            self.request.sendall("-1")


class SparkCLSlaveServer(SocketServer.TCPServer):
    def server_activate(self):
        #print "SparkCL Slave is running."
        SocketServer.TCPServer.server_activate(self)
        return


class GetSlaveData():
    global json_data
    global sparkcl_slaves
    global platform_counter
    for platform in cl.get_platforms() :
        platform_counter = platform_counter + 1
        device_counter = 0
        for device in platform.get_devices():
             json_data.append({"name":device.name.strip()})
             sparkcl_slaves.append(SlaveController.SlaveController(platform_counter,device_counter,platform.name,device.name))
             device_counter = device_counter + 1
    json_data = json.dumps(json_data)

class RegistSlave():
    pass

if __name__ == "__main__":

    #print json_data
    #HOST = "localhost"
    #PORT = 9001

    os.environ['SPARK_HOME'] = sys.argv[3]
    try :
        print "Connect to %s:%s" %(master_ip,9000)
        s = socket.socket()
        s.connect((master_ip, 9000))
    except :
        print "Can't connect to master."
        sys.exit();
    GetSlaveData()
    #SlaveINFO()
    try :
        server = SparkCLSlaveServer((HOST, 0), MyTCPHandler)
        print "SparkCL Slave is running"
        print HOST+":"+str(server.socket.getsockname()[1])
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    except :
        raise
    finally :
        s.close();
        print "End."

        #server.shutdown()
#    HOST, PORT = "10.20.22.206", 10001
#    server = SparkClServer((HOST, PORT), MyTCPHandler);
#    try:
#        server.serve_forever()
#    except:
#        server.socket.close()
