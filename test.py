import subprocess
import re
import socket
netstat = subprocess.Popen(["netstat -an | grep :7077"], stdout=subprocess.PIPE, shell=True)
(out, err) = netstat.communicate()
out = out.split('\n');
print "WORKER-IP                          SPARKCL "
for s in out:
    matchObj = re.match( r'^.+ (.+):7077\s+(\S+):.+ESTABLISHED$',s, re.M|re.I)

    if matchObj:
        #print s
        #print "master: "+ matchObj.group(1)
        HOST, PORT = matchObj.group(2), 10001
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((HOST, PORT))
            print  matchObj.group(2) + "                         OK"
            sock.close()
        except:
            print HOST+"not have sparkcl."

#print out
