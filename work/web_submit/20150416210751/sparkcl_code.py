from sparkcl import SparkCLContext ,SparkCLKernel , SparkCL
if __name__ == "__main__" : 
	work_path = "/home/job/spark-1.2.0/sparkcl/work/web_submit/20150416210751"
	s_cl = SparkCL("job1","192.168.12.10")
	kernel0 = SparkCLKernel(work_path+"/kernel/0.cl",work_path+"/xml/0.xml",output_type="int")
	s_cl.addKernel(kernel0,type="map")
	data = []
	print s_cl.run(data)