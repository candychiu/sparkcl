#SparkCL
Parallel Computing (OpenCL) + Distributed Computing (Apache Spark)
#Installation
`sudo apt-get install freeglut3-dev libboost-all-dev build-essential`

Download intel SDK

`wget http://registrationcenter.intel.com/irc_nas/4181/intel_sdk_for_ocl_applications_2014_ubuntu_4.4.0.117_x64.tgz`

Download intel SDK setup patch and install intel sdk

https://drive.google.com/file/d/0BwREp2vz9v5xbTk2QjNQNFI0VTQ/edit?usp=sharing

Install PyOpenCL

http://wiki.tiker.net/PyOpenCL/Installation/Linux

#How to use
start master $ ./sbin/start-sparkcl-master [ip address]

start slave $  ./sbin/start-sparkcl-slaves [slave ip] [master ip]

#Copyright and license
Chiang Mai University Thailand
