from sparkcl import SparkCLContext ,SparkCLKernel , SparkCL
if __name__ == "__main__" : 
	work_path = "/home/job/spark-1.2.0/sparkcl/work/web_submit/20150422184605"
	s_cl = SparkCL("job1","10.20.20.168")
	kernel0 = SparkCLKernel("kernel0",work_path+"/kernel/0.cl",work_path+"/xml/0.xml",output_type="int")
	s_cl.addKernel(kernel0,type="map")
	kernel1 = SparkCLKernel("kernel1",work_path+"/kernel/1.cl",work_path+"/xml/1.xml",output_type="int")
	s_cl.addKernel(kernel1,type="reduce")
	data = []
	print s_cl.run(data)