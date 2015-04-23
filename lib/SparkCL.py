#from pyspark import SparkContext, SparkConf
import os
import sys
import pyopencl as cl
import numpy as np
import subprocess
import xml.etree.ElementTree as ET
import re
import time

class SparkCL :

	def __init__(self) :
		self.kernel = []
		self.spark_master = ""
		self.app_name = ""
	def setMaster (self,spark_master) :
		self.spark_master = spark_master

	def setAppName (self,app_name) :
		self.app_name = app_name

	def AddKernel (self,_kernel):

		try :
			self.kernel.append(_kernel)
		except :
			raise
		#print len(self.kernel)

	def GetAllKernel(self):
		return self.kernel

	def Run (self,data_file) :


		## HEADER

		header_template = open('header-template','r').read()
		## MAP FUNCTION 
		
   		map_template = open('map-template','r').read()
   		kernel_counter = 0
   		all_map_code = ""
		for k in self.kernel :

			data_counter = 0
			init_array_part = ""
   			enqueue_arg = ""
			kernel_counter = kernel_counter + 1
			config = k.getConfig()

			for argv in config['arguments'] :
				matchObj = re.match( r'\$(data\[\d+\])', argv, re.M|re.I)
				if matchObj :
					init_array_part = init_array_part + "    np_data.append(np.array("+matchObj.group(1)+").astype(np.float32))\n"
					init_array_part = init_array_part + "    data_buf.append(cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np_"+matchObj.group(1)+"))\n"
					enqueue_arg = enqueue_arg + ",data_buf[" + str(data_counter) + "]"
					data_counter=data_counter+1
				
					continue

				matchObj = re.match( r'\$result\Z', argv, re.M|re.I)
				if matchObj:
					enqueue_arg = enqueue_arg + ",result_buf"
					continue

				matchObj = re.match( r'^\d+\Z', argv, re.M|re.I)
				if matchObj:
					enqueue_arg = enqueue_arg + ",np.uint32(" + str(argv) +")"
					continue
					
			#print init_array_part
			map_code = map_template % ('map'+str(kernel_counter),k.kernel_code,k.kernel_name,init_array_part,k.output_dim,k.local_work_size,enqueue_arg)
			all_map_code = all_map_code + map_code + '\n\n'
			#print map_code
			#print '\n\n'

		## REDUCE FUNCTION
		## --- IN PROGRESS ---

		## MAIN FUNCTION
		main_template = open("main-template","r").read()
		kernel_counter = 0
		parallelize_part = ""
		for k in self.kernel :
			kernel_counter = kernel_counter + 1
			if k.kernel_type == 'map' :
				parallelize_part = parallelize_part + ".map(map"+str(kernel_counter)+")"
			else :
				parallelize_part = parallelize_part + ".reduce(reduce"+str(kernel_counter)+")"
		main_code = main_template % (self.app_name,self.spark_master,data_file.replace('\n',''),parallelize_part)
		#print parallelize_part
		sparkcl_code_file = open("sparkcl_tmp.py","w")
		sparkcl_code_file.write(header_template+'\n'+all_map_code+"\n"+main_code)

		return 
	def GetKernel (self,idx):
		return self.kernel[idx]

	def SetKernel (self,type,kernel_code,kernel_setting,data_file):
		pass




class Kernel :

	def __init__(self,kernel_name,kernel_code=None,xml_string=None,kernel_type=None) :

		self.kernel_name = kernel_name
		#self.kernel_code = ""
		
		if kernel_code is None :
			self.kernel_code = ""
		else :
			self.loadKernel(kernel_code)

		if xml_string is None :
			self.output_dim = ""
			self.local_work_dim = ""
			self.global_work_dim = ""
			self.arguments = []
		else :
			self.loadXMLConfig(xml_string)

		if kernel_type is None :
			self.kernel_type = 'map'
		else : 
			self.kernel_type = kernel_type
	def getKernelCode (self) :
		return self.kernel_code
	def gerKernelName (self) :
		return self.kernel_name
	def loadKernel (self,code) :
		self.kernel_code = code

	def loadXMLConfig (self,xml_string) :

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


	def printKernelInfo(self) :
		print "output_dim :",self.output_dim
		print "arguments :",self.arguments
		print "local_work_size :",self.local_work_size

	def  getConfig(self) :
		return {"output_dim":self.output_dim , "arguments":self.arguments,"local_work_size":self.local_work_size}



#class SparkCLSubmit :
