from sparkcl import SparkCLContext ,SparkCLKernel , SparkCL

if __name__ == "__main__" :


	kernel1 = SparkCLKernel("kernel.cl","kernel_conf.xml",output_type='int')
	kernel2 = SparkCLKernel("kernel2.cl","kernel2_conf.xml",output_type='int')
	kernel3 = SparkCLKernel("kernel3.cl","kernel3_conf.xml",output_type='int')
	kernel4 = SparkCLKernel("kernel4.cl","kernel4_conf.xml",output_type='int')
	kernel5 = SparkCLKernel("kernel5.cl","kernel5_conf.xml",output_type='int')


	s_cl = SparkCL("job1","10.20.22.107")
	s_cl.addKernel(kernel3)
	#s_cl.addKernel(kernel5,'reduce')


	data = [ (1,[[1,2,3],[3,4,5]]) , (1,[[1,2,3],[3,4,5]]) ]
	print s_cl.run(data)