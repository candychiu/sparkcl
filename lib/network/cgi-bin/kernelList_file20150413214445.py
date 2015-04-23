from sparkcl import SparkCLContext ,SparkCLKernel , SparkCL
if __name__ == "__main__" : 
	s_cl = SparkCL("job1","192.168.1.40")
	kernel0 = SparkCLKernel("kernelList_file/1","kernelList_file/1.xml",output_type="int")
	s_cl.addKernel(kernel0,type="map")
	data = [[1,2,3,4,5]]
	print s_cl.run(data)