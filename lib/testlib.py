import SparkCL

s_cl = SparkCL.SparkCL()
s_cl.setAppName("MyApp")
s_cl.setMaster("10.20.21.194")

kernel_code = open('testfile/1.cl','r').read()
xml_string  = open('testfile/1.xml','r').read()
s_cl.AddKernel(SparkCL.Kernel('ArraySum',kernel_code,xml_string))

kernel_code = open('testfile/2.cl','r').read()
xml_string  = open('testfile/2.xml','r').read()
s_cl.AddKernel(SparkCL.Kernel('Mul2',kernel_code,xml_string))


data = open('testfile/data.txt','r').read()

s_cl.Run(data)

