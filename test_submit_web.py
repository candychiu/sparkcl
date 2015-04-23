import sys 

kernel_code = ""
kernel_code = kernel_code + "from sparkcl import SparkCLContext ,SparkCLKernel , SparkCL\n"
kernel_code = kernel_code + 'if __name__ == "__main__" : \n'
sparkcl_lib_path = "lib/network/cgi-bin/kernelList_file"

for i in range(1,len(sys.argv)) :
	kernel_code = kernel_code + '\t' + 'kernel%s = SparkCLKernel("%s","%s.xml",output_type="int")\n'%(i,str(sys.argv[i]),str(sys.argv[i]))
	kernel_code = kernel_code + '\t' + 's_cl.addKernel(kernel%s,type="%s")\n'%(i,"map")


kernel_code = kernel_code + '\t' + 'data = '
kernel_code = kernel_code + '\t' + 'print s_cl.run(data)'

print kernel_code
