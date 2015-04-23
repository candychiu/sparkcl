import subprocess
import os
proc = subprocess.Popen(["../bin/get-host-platform-device.sh"], stdout=subprocess.PIPE, shell=True)
(proc_out, err) = proc.communicate()
[SPARKCL_PLATFORM , SPARKCL_DEVICE] = proc_out.split()
print "SPARKCL_PLATFORM = "+SPARKCL_PLATFORM
print "SPARKCL_DEVICE   = "+SPARKCL_DEVICE
