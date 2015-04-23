#!/usr/bin/env python

import SocketServer
import re

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        #print "Connect"
        while True:
            try:
                self.data = self.request.recv(1024).strip()
                if self.data=="":
                    break
                print ">> "+str(self.data)
                matchObj = re.match( r'set_platform_device\[(\S+),(\S+)\]', self.data , re.M|re.I)
                if matchObj :
                    print ">>>> Platform : "+str(matchObj.group(1))
                    print ">>>> Device : " +str(matchObj.group(2))
                #print "{} wrote:".format(self.client_address[0])

            except:
                raise
                break

        # just send back the same data, but upper-cased
        #self.request.sendall(self.data.upper())

class SparkClServer(SocketServer.ThreadingTCPServer):
    def verify_request(self, request, client_address):
        print client_address , "connected"
        ###########################################
        #                                         #
        #   Do Something when client connected    #
        #                                         #
        ###########################################
        return SocketServer.TCPServer.verify_request(self, request, client_address)
    def close_request(self, request_address):
        print request_address , "closed"
        ###########################################
        #                                         #
        #   Do Something when client disconnect   #
        #                                         #
        ###########################################
        return SocketServer.TCPServer.close_request(self, request_address)



if __name__ == "__main__":
    HOST, PORT = "10.20.22.206", 10001
    server = SparkClServer((HOST, PORT), MyTCPHandler);
    try:
        server.serve_forever()
    except:
        server.socket.close()
