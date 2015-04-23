from pyspark import SparkContext, SparkConf
import os
import sys
import pyopencl as cl
import numpy as np
import subprocess
def map1(data):

    SPARKCL_PLATFORM = os.environ['CL_PLATFORM']
    SPARKCL_DEVICE = os.environ['CL_DEVICE']
    print str(SPARKCL_PLATFORM)+":"+str(SPARKCL_DEVICE)
    KERNEL_CODE="""
        __kernel void ArraySum(__global float *A,__global float *B,__global float *C){
       int i = get_global_id(0);
       C[i] = A[i]+B[i];
}

    """

    cl_device=cl.get_platforms()[int(SPARKCL_PLATFORM)].get_devices()[int(SPARKCL_DEVICE)]
    ctx = cl.Context([cl_device])
    queue = cl.CommandQueue(ctx)
    prg = cl.Program(ctx, KERNEL_CODE).build()
    kernel = prg.ArraySum
    mf = cl.mem_flags
    print "map" + str(data)

    np_data = []
    data_buf = []
    np_data.append(np.array(data[0]).astype(np.float32))
    data_buf.append(cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np_data[0]))
    np_data.append(np.array(data[1]).astype(np.float32))
    data_buf.append(cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np_data[1]))

    result = np.zeros((5,)).astype(np.float32)
    result_buf = cl.Buffer(ctx, mf.WRITE_ONLY, result.nbytes)

    kernel(queue,(5,),None,data_buf[0],data_buf[1],result_buf)
    cl.enqueue_read_buffer(queue, result_buf, result).wait()
    return [result.astype(np.float32)]


def map2(data):

    SPARKCL_PLATFORM = os.environ['CL_PLATFORM']
    SPARKCL_DEVICE = os.environ['CL_DEVICE']
    print str(SPARKCL_PLATFORM)+":"+str(SPARKCL_DEVICE)
    KERNEL_CODE="""
        __kernel void Mul2(__global float *A,__global float *B){
       int i = get_global_id(0);
       B[i] = A[i]+A[i];
}

    """

    cl_device=cl.get_platforms()[int(SPARKCL_PLATFORM)].get_devices()[int(SPARKCL_DEVICE)]
    ctx = cl.Context([cl_device])
    queue = cl.CommandQueue(ctx)
    prg = cl.Program(ctx, KERNEL_CODE).build()
    kernel = prg.Mul2
    mf = cl.mem_flags
    print "map" + str(data)

    np_data = []
    data_buf = []
    np_data.append(np.array(data[0]).astype(np.float32))
    data_buf.append(cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np_data[0]))

    result = np.zeros((5,)).astype(np.float32)
    result_buf = cl.Buffer(ctx, mf.WRITE_ONLY, result.nbytes)

    kernel(queue,(5,),None,data_buf[0],result_buf)
    cl.enqueue_read_buffer(queue, result_buf, result).wait()
    return [result.astype(np.float32)]



if __name__ == "__main__" :
	try:
		conf = SparkConf().setAppName("MyApp").setMaster("spark://10.20.21.194:7077")
		conf.set("spark.scheduler.allocation.file", "conf/fairscheduler.xml")
		sc = SparkContext(conf=conf)
		sc.setLocalProperty("spark.scheduler.pool", "pool1")
		distData = sc.parallelize([[[[1,2,3,4,5],[1,2,3,4,5]]]]).map(map1).map(map2)
		result = distData.collect()
		for r in result :
			print r[0].tolist()
	except:
		raise