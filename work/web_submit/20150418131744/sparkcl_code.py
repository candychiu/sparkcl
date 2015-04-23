from sparkcl import SparkCLContext ,SparkCLKernel , SparkCL
if __name__ == "__main__" : 
	work_path = "/home/job/spark-1.2.0/sparkcl/work/web_submit/20150418131744"
	s_cl = SparkCL("job1","10.20.22.107")
	kernelkernel0 = SparkCLKernel("0",work_path+"/kernel/0.cl",work_path+"/xml/0.xml",output_type="int")
	s_cl.addKernel(kernel0,type="map")
	data = []
	print s_cl.run(data)