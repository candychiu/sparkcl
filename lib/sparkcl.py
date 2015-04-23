from pyspark import SparkContext, SparkConf , RDD
import pyopencl as cl
import numpy as np
import xml.etree.ElementTree as ET
import re
import time
from datetime import datetime, date
import sqlite3
import os
import platform
import sys
import signal

class SparkCL  :

	def __init__(self,app_name,master_ip) :
		self.kernel_list = []
		self.sc = SparkCLContext(app_name,master_ip)
		self.kernel_count = 0

	def addKernel (self,kernel,type=None) :
		self.kernel_list.append((kernel,type))

	def run (self,data) :

		distData = self.sc.Submit(data)
		for k in self.kernel_list :
			print k[0], " ", k[1]
			distData = distData.addKernel(k[0],k[1])
		return distData.run()

class SparkCLContext(SparkContext):
	
	def __init__(self, app_name,master_ip):
		
		conn = sqlite3.connect(os.environ['SPARKCL_HOME']+'/lib/network/cgi-bin/system.db')
		maxID_t = conn.execute("select max(id) from job")
		for row in maxID_t:
			maxID, = row

		if maxID is None :
			maxID = 1

		conn.close()
		
		self.app_id = maxID + 1;
		self.app_name = app_name

		conf = SparkConf().setAppName(app_name).setMaster("spark://"+master_ip+":7077").set("spark.akka.frameSize", "100").set("spark.serializer","org.apache.spark.serializer.KryoSerializer")
		super(SparkCLContext, self).__init__(conf=conf)
		#self.addPyFile("sparkcl.py")
		#sc.setLocalProperty("spark.scheduler.pool", "pool1")
	def Submit(self,*argv) :

		def run(self) :
			def sigterm_handler(_signo, _stack_frame):
				# Raises SystemExit(0):
				conn = sqlite3.connect(os.environ['SPARKCL_HOME']+'/lib/network/cgi-bin/system.db')
				conn.execute("update job set isComplete=%s,finish_time='%s' where id = %s" %(2,datetime.now().replace(microsecond=0),maxID))
				conn.commit()
				conn.close()
				sys.exit(0)
			########################
			self.pid = os.getpid()
			conn = sqlite3.connect(os.environ['SPARKCL_HOME']+'/lib/network/cgi-bin/system.db')
			conn.execute("insert into job (name,submit_time,isComplete) values(?,?,0)",(self.app_name,datetime.now().replace(microsecond=0)))
			maxID_t = conn.execute("select max(id) from job")

			for row in maxID_t:
				maxID, = row

			if maxID is None :
				maxID = 1

			conn.execute("update job set pid=%s where id=%s"%(self.pid,maxID))
			conn.commit()
			conn.close()
			print self.pid
			signal.signal(signal.SIGTERM, sigterm_handler)
			########################
			isComplete = 1
			try:

				start_time = time.time();
				output =  self.values().collect()
				self.run_time = time.time() - start_time;
			
			except KeyboardInterrupt :
				output = "KeyboardInterrupt";
				isComplete = 2

			except Exception as e:
				output = e
				isComplete = 3

			########################
			
			conn = sqlite3.connect(os.environ['SPARKCL_HOME']+'/lib/network/cgi-bin/system.db')
			conn.execute("update job set isComplete=%s,finish_time='%s' where id = %s" %(isComplete,datetime.now().replace(microsecond=0),maxID))
			conn.commit()
			conn.close()
			
			########################

			with open(os.environ['SPARKCL_HOME']+"/lib/network/cgi-bin/output_file/"+str(maxID), "w") as output_file:
				output_file.write(str(output))

			if not os.path.exists(os.environ['SPARKCL_HOME']+"/lib/network/cgi-bin/kernel_file/"+str(maxID)):
				os.makedirs(os.environ['SPARKCL_HOME']+"/lib/network/cgi-bin/kernel_file/"+str(maxID))
			k_count = 0
			for k in self.kernel_code_list :
				kernel_file = open(os.environ['SPARKCL_HOME']+"/lib/network/cgi-bin/kernel_file/"+str(maxID)+"/"+str(k_count), "w")
				kernel_file.write(k)
				k_count = k_count + 1

			return output 

		def mapCL(self,argv) :
			return RDD.map(self,argv.map)

		def mapValuesCL(self, argv) :
			return RDD.mapValues(self,argv.map)

		def reduceByKeyCL(self,argv) :
			return RDD.reduceByKey(self,argv)
		
		def addKernel(self,argv,type=None) :
			
			self.kernel_code_list.append(argv.kernel_code)
			argv.app_id = self.app_id
			if (type is None) or (type == 'map') :
				print 'map'
				return RDD.mapValues(self,argv.map)			
			else :
				print 'reduce'
				return RDD.reduceByKey(self,argv.reduce)

		RDD.app_id = self.app_id
		RDD.kernel_code_list = []
		RDD.run = run	
		RDD.addKernel = addKernel
		RDD.mapCL = mapCL
		RDD.reduceByKeyCL = reduceByKeyCL
		RDD.mapValuesCL = mapValuesCL
		RDD.app_name = self.app_name
		#print argv
		sc = SparkContext.parallelize(self,*argv)
		return sc


	def kkk(self,a):
		return "hello"
	def mapJob(self,argv) :
		#print "Hello"
		super(SparkCLContext,self).map(argv)


class SparkCLKernel  (object):
	def __init__ (self,kernel_name,kernel_file,xml_file=None,**kwargs) :
		self.kernel_code = open(kernel_file,'r').read()
		self.kernel_name = kernel_name
		self.slave_name = platform.node()
		if 'output_type' in kwargs :
			if not(kwargs['output_type'] is None) :
				if kwargs['output_type'] == 'float' :
					self.out_type = np.float32
				elif kwargs['output_type'] == 'int' :
					self.out_type = np.int32
			else :
				self.out_type = np.float32
		else :
			self.out_type = np.float32

		if not(xml_file is None) :
			try :
				self.loadXMLConfig(xml_file)
			except :
				raise

		idx1 = self.kernel_code.find('(')
		idx2 = self.kernel_code[0:idx1].rfind(' ')
		self.function_name = self.kernel_code[idx2+1:idx1]

	def reduce (self,data1,data2) :
		KERNEL_CODE = self.kernel_code

		cl_device=cl.get_platforms()[int(0)].get_devices()[int(0)]
		ctx = cl.Context([cl_device])
		queue = cl.CommandQueue(ctx)
		prg = cl.Program(ctx, KERNEL_CODE).build()
		#kernel = prg.ArraySum
		kernel = getattr(prg, self.function_name )
		mf = cl.mem_flags

		print "reduce " + str(data1)
		print "and " + str(data2)
		

		np_data = []
		data_buf = []
		args = []
		arg_count = 0

		result = np.zeros(self.output_dim).astype(np.int32)
		result_buf = cl.Buffer(ctx, mf.WRITE_ONLY, result.nbytes)

		##ARGUMENT PART
		for argv_str in self.arguments :

			#DATA
			if argv_str == "$data1" :
				np_data.append(np.array(data1).astype(np.int32))
				data_buf.append(cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np_data[arg_count]))
				args.append(data_buf[arg_count])
				arg_count = arg_count + 1
				continue 

			if argv_str == "$data2" :
				np_data.append(np.array(data2).astype(np.int32))
				data_buf.append(cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np_data[arg_count]))
				args.append(data_buf[arg_count])
				arg_count = arg_count + 1
				continue 


			matchObj = re.match( r'\$(data1\[(\d+)\])', argv_str, re.M|re.I)
			if matchObj :
				idx = int(matchObj.group(2))
				np_data.append(np.array(data1[idx]).astype(np.int32))
				data_buf.append(cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np_data[arg_count]))
				args.append(data_buf[arg_count])
				arg_count = arg_count + 1
				continue

			matchObj = re.match( r'\$(data2\[(\d+)\])', argv_str, re.M|re.I)
			if matchObj :
				idx = int(matchObj.group(2))
				np_data.append(np.array(data2[idx]).astype(np.int32))
				data_buf.append(cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np_data[arg_count]))
				args.append(data_buf[arg_count])
				arg_count = arg_count + 1
				continue
			
			#RESULT
			matchObj = re.match( r'\$result\Z', argv_str, re.M|re.I)
			if matchObj :
				args.append(result_buf)
				continue

			#NUMBER
			matchObj = re.match( r'^\d+\Z', argv_str, re.M|re.I)
			if matchObj :
				args.append(np.int32(matchObj.group(0)))
				continue


		args = tuple(args)
		print args
		kernel(queue,self.global_work_size,self.local_work_size,*args)
		cl.enqueue_read_buffer(queue, result_buf, result).wait()

		print result
		return result.astype(self.out_type).tolist()
		return 1


	def map (self,data) :
		print self.slave_name
		KERNEL_CODE = self.kernel_code

		cl_device=cl.get_platforms()[int(os.environ['CL_PLATFORM'])].get_devices()[int(os.environ['CL_DEVICE'])]
		ctx = cl.Context([cl_device])
		queue = cl.CommandQueue(ctx)
		prg = cl.Program(ctx, KERNEL_CODE).build()
		#kernel = prg.ArraySum

		kernel = getattr(prg, self.function_name )
		mf = cl.mem_flags

		self.sendLog("MAP,KERNEL:%s size= %s byte(s)"%(self.kernel_name,str(sys.getsizeof(data))))
		print "map" + str(data)

		np_data = []
		data_buf = []
		args = []
		arg_count = 0

		result = np.zeros(self.output_dim).astype(np.int32)
		result_buf = cl.Buffer(ctx, mf.WRITE_ONLY, result.nbytes)

		##ARGUMENT PART
		for argv_str in self.arguments :

			#DATA
			if argv_str == "$data" :
				np_data.append(np.array(data).astype(np.int32))
				data_buf.append(cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np_data[arg_count]))
				args.append(data_buf[arg_count])
				arg_count = arg_count + 1
				continue 
			matchObj = re.match( r'\$(data\[(\d+)\])', argv_str, re.M|re.I)
			if matchObj :
				idx = int(matchObj.group(2))
				np_data.append(np.array(data[idx]).astype(np.int32))
				data_buf.append(cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np_data[arg_count]))
				args.append(data_buf[arg_count])
				arg_count = arg_count + 1
				continue
			
			#RESULT
			matchObj = re.match( r'\$result\Z', argv_str, re.M|re.I)
			if matchObj :
				args.append(result_buf)
				continue

			#NUMBER
			matchObj = re.match( r'^\d+\Z', argv_str, re.M|re.I)
			if matchObj :
				args.append(np.int32(matchObj.group(0)))
				continue

		args = tuple(args)
		print args
		kernel(queue,self.global_work_size,self.local_work_size,*args)
		cl.enqueue_read_buffer(queue, result_buf, result).wait()

		print result
		return result.astype(self.out_type).tolist()

	def loadXMLConfig (self,xml_file) :

		xml_string = open(xml_file,'r').read()
		root = ET.fromstring(xml_string)

		try :
			output_dim  = root.find('output_dim')
			self.output_dim = output_dim.text
		except :
			print "ERROR : Can't find <output_dim> in XML file."
		
		try :
			arguments  = root.find('arguments')
			self.arguments = arguments.text.split(',')
		except :
			print "ERROR : Can't find <arguments> in XML file."
		
		try :
			local_work_size  = root.find('local_work_size')
			self.local_work_size = local_work_size.text
		except :
			print "ERROR : Can't find <local_work_size> in XML file."

		try :
			global_work_size  = root.find('global_work_size')
			self.global_work_size = global_work_size.text
		except :
			print "ERROR : Can't find <global_work_size> in XML file."

		if not(self.output_dim is None):
			self.output_dim = tuple(map(int,self.output_dim.split(',')))
		if not(self.local_work_size is None):
			self.local_work_size = tuple(map(int,self.local_work_size.split(',')))
		if not(self.global_work_size is None):
			self.global_work_size = tuple(map(int,self.global_work_size.split(',')))

	def printConf (self) :
		print 'Result size :',self.output_dim
		print 'Arguments :',self.arguments
		print 'local_work_size :', self.local_work_size
		print 'global_work_size :', self.global_work_size


	def sendLog (self,log_string) :
		with open(os.environ['SPARKCL_HOME']+"/work/log/slaves/"+os.environ['CL_PLATFORM']+"_"+os.environ['CL_DEVICE']+"/"+str(self.app_id)+".txt", "a") as myfile:
			myfile.write(log_string+'\n')



class SparkCLWebKernel (SparkCLKernel) :
	def __init__ (self,kernel_name,xml_file) :
		#print "Hello"
		try:
			conn = sqlite3.connect(os.environ['SPARKCL_HOME']+'/lib/network/cgi-bin/system.db')
			db = conn.execute("select * from job_list where name = '%s'"%kernel_name)
			for row in db :
				pass
			kernel_file = str(os.environ['SPARKCL_HOME']+'/lib/network/cgi-bin/kernelList_file/'+str(row[0]))
		except :
			print "Can't find kernel"
		super(SparkCLWebKernel, self).__init__(kernel_name,kernel_file,xml_file)