#!/usr/bin/env python

import os
import sys
import time
import subprocess

master_ip = sys
getNohupID = subprocess.Popen(["nohup /home/job/spark-1.2.0/bin/spark-class org.apache.spark.deploy.worker.Worker spark://10.20.22.206:7077 > /dev/null 2>&1 & echo $!"], stdout=subprocess.PIPE, shell=True)
(nohupID, err) = getNohupID.communicate()
nohupID = int(nohupID.strip('\n'))

counter = 0
while True;

    p = subprocess.Popen("netstat -an | grep :7077", stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    print output
    time.sleep(1)

print nohupID
