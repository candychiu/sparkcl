from sparkcl import SparkCLContext ,SparkCLKernel , SparkCL ,SparkCLWebKernel
import os
if __name__ == "__main__" :

	print os.getpid()
	kernel1 = SparkCLWebKernel('sum',"kernel9_conf.xml")
	kernel2 = SparkCLKernel('job1','kernel2.cl','kernel2_conf.xml')
	kernel3 = SparkCLKernel('job2','kernel3.cl','kernel3_conf.xml')
	s_cl = SparkCL("job1","10.20.22.107")
	s_cl.addKernel(kernel1)
	s_cl.addKernel(kernel2)
	#s_cl.addKernel(kernel3,'reduce')

	data = [ (1,[[1,2,3,4,5],[1,2,3,4,5]]) , (1,[[1,2,3,4,5],[1,2,3,4,5]]) ]
	print s_cl.run(data)