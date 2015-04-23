#!/usr/bin/env python
import shutil
import os
import sys
import time
import subprocess
import re

class SlaveController :

    def __init__(self,platform_id,device_id,platform_name,device_name):
        self.SlaveID = 0;
        self.platform_id = platform_id
        self.device_id = device_id
        self.platform_name = platform_name.strip()
        self.device_name = device_name.strip()

    def start(self,master_ip):
        spark_home = os.environ['SPARK_HOME']
        sparkcl_home = spark_home+'/sparkcl'
        if self.SlaveID != 0 :
            return 0

        #create Log folder    
        log_path = sparkcl_home+'/work/log/slaves/'+str(self.platform_id)+'_'+str(self.device_id)
        if not os.path.exists(log_path):
            os.makedirs(log_path)
            os.chmod(log_path,0777)
        else :
            shutil.rmtree(log_path)
            os.makedirs(log_path)
            os.chmod(log_path,0777)
        #print "nohup "+spark_home+"/bin/spark-class org.apache.spark.deploy.worker.Worker spark://"+master_ip+":7077 -c 1 > /dev/null 2>&1 & echo $!"
        export_str = "export CL_DEVICE=%s; " %(self.device_id)
        export_str = export_str + "export CL_PLATFORM=%s; " %(self.platform_id)
        export_str = export_str + "export SPARKCL_HOME=%s; " %(sparkcl_home)
        getNohupID = subprocess.Popen([export_str + "nohup "+spark_home+"/bin/spark-class org.apache.spark.deploy.worker.Worker spark://"+master_ip+":7077 -c 1 > /dev/null 2>&1 & echo $!"], stdout=subprocess.PIPE, shell=True)
        (nohupID, err) = getNohupID.communicate()
        #print err
        nohupID = int(nohupID.strip('\n'))
        counter = 0

        try :
            while counter < 5:
                counter = counter + 1
                p = subprocess.Popen("netstat -anp | grep %s" % (nohupID), stdout=subprocess.PIPE, shell=True)
                (curr_netstat, err) = p.communicate()
                curr_netstat = curr_netstat.split('\n')
                time.sleep(2)
                check_est = False
                check_lis = False
                for s in curr_netstat:

                    matchEst = re.match( r'.+\s+(\d+.\d+.\d+.\d+):\S+\s+(\S+):7077.+ESTABLISHED\s+%s/java.*\Z'%(nohupID),s, re.M|re.I)
                    matchLis = re.match( r'.+\s+(\d+.\d+.\d+.\d+):\S+\s+(\S+):\S+.+LISTEN\s+%s/java.*\Z'%(nohupID),s, re.M|re.I)

                    if matchLis :
                        check_est = True
                    if matchEst :
                        check_lis = True

                if check_lis and check_est :
                    break
            if check_lis and check_est :
                self.SlaveID = nohupID
                return 1

            else :
                raise

        except :
            subprocess.call(["kill", str(nohupID)])
            return 0
    def stop(self):
        if self.SlaveID != 0 :
            subprocess.call(["kill",str(self.SlaveID)])
            self.SlaveID = 0
        return 1;

    def isAlive(self):
        if self.SlaveID != 0 :
            return 1
        return 0

    def printINFO(self):
        print "PLATFORM: " + self.platform_name
        print "DEVICE: " + self.device_name
    #netstat -anp | grep PID
