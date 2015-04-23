#!/usr/bin/env python

import os
import sys
import re

def test():
    print "TINTHID"

def loadKernel(kernel_path):
    KERNEL_FILE = open(kernel_path,"r");
    return KERNEL_FILE.read()

def genHeader():
    header_template = open(SPARKCL_PATH+"/lib/header-template","r")
    header_code = header_template.read()
    return header_code

def genMapFunction(kernel_code,SPARKCL_PATH,map_arg):
    idx1 = kernel_code.find('(')
    idx2 = kernel_code[0:idx1].rfind(' ')
    function_name = kernel_code[idx2+1:idx1]

    map_template = open(SPARKCL_PATH+"/lib/map-template","r")
    map_code = map_template.read()

    arg_conf = map_arg.split()
    data_counter = 0


    init_array_part = ""
    enqueue_arg = ""

    for argv in arg_conf :
        matchObj = re.match( r'\$(data\[\d+\])', argv, re.M|re.I)
        if matchObj:
            #print argv
            init_array_part = init_array_part + "    np_data.append(np.array("+matchObj.group(1)+").astype(np.float32))\n"
            init_array_part = init_array_part + "    data_buf.append(cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=np_"+matchObj.group(1)+"))\n"
            enqueue_arg = enqueue_arg + ",data_buf[" + str(data_counter) + "]"
            data_counter=data_counter+1
            continue

        matchObj = re.match( r'\$result\Z', argv, re.M|re.I)
        if matchObj:
            #print argv
            enqueue_arg = enqueue_arg + ",result_buf"
            continue

        matchObj = re.match( r'^\d+\Z', argv, re.M|re.I)
        if matchObj:
            #print argv
            enqueue_arg = enqueue_arg + ",np.uint32(" + str(argv) +")"
            continue


    wf = open("../../../work/temp/work_item.txt","r");
    rf = open("../../../work/temp/result_size.txt","r");

    return map_code % (kernel_code,function_name,init_array_part,rf.read().replace('\n',''),wf.read().replace('\n',''),enqueue_arg)

def genMainFunction(app_name,spark_master_ip):
    main_template = open(SPARKCL_PATH+"/lib/main-template","r")
    main_code = main_template.read()
    data_file = open(SPARKCL_PATH+"/work/temp/data.txt")
    data_str = data_file.read().replace('\n','')
    return main_code % (app_name,spark_master_ip,data_str)

if __name__ == "__main__" :

    try:
        APP_ID       = sys.argv[1]
        SPARKCL_PATH = sys.argv[2]
        SPARK_MASTER_IP = sys.argv[3]
        SUBMIT_TIME = sys.argv[4]
        MAP_ARG_CONF = sys.argv[5]
        #KERNEL_FILENAME = sys.argv[5]
        KERNEL_FILENAME = "kernel.cl"
        SPARKCL_CODE = ""

        MAP_CONF_FILE = open(SPARKCL_PATH+"/work/temp/map_argv.txt","r")
        MAP_ARG_CONF = MAP_CONF_FILE.read().replace('\n','')
        #print "APP_ID        = "+str(APP_ID)
        #print "SPARKCL_PATH  = "+str(SPARKCL_PATH)
        #print "MAP ARG CONF  = "+str(MAP_ARG_CONF)
        KERNEL_CODE = loadKernel(SPARKCL_PATH+"/work/temp/"+KERNEL_FILENAME)

        SPARKCL_CODE = SPARKCL_CODE + str(genHeader()) + "\n";
        SPARKCL_CODE = SPARKCL_CODE + str(genMapFunction(KERNEL_CODE,SPARKCL_PATH,MAP_ARG_CONF)) + "\n";
        SPARKCL_CODE = SPARKCL_CODE + str(genMainFunction("test_app","spark://"+SPARK_MASTER_IP+":7077")) + "\n";
        #print "SUCCESS"

        #SPARKCL_CODE_FILE = open(SPARKCL_PATH+"/work/code_test.py","w")
        #SPARKCL_CODE_FILE.write(SPARKCL_CODE)
        SPARKCL_CODE_FILE = open(SPARKCL_PATH+"/work/code_"+SUBMIT_TIME+".py","w")
        SPARKCL_CODE_FILE.write(SPARKCL_CODE)
        ##Generate Map Code
        #MAP_CODE =

    except:
        raise
