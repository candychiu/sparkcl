#!/usr/bin/env python
import time
import datetime
import cgi
import os
import cgitb; cgitb.enable()
import subprocess
from shutil import copyfile 

st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')

def fbuffer(f, chunk_size=10000):
   while True:
      chunk = f.read(chunk_size)
      if not chunk: break
      yield chunk

form = cgi.FieldStorage()
numKernel = form.getvalue('numKernel')
file_data = form.getvalue('file')
app_name = form.getvalue('app_name')

save_path =  os.environ['SPARKCL_HOME']+'/work/web_submit/'+str(st)
os.makedirs(save_path)
os.makedirs(save_path+'/xml')
os.makedirs(save_path+'/kernel')
print """Content-type: text/html

"""
open(os.environ['SPARKCL_HOME']+'/work/log/master/logs.txt','a').write('%s - Submit application app_name=%s\n'%(time.strftime("%H:%M:%S"),app_name))
#print 'Submit timestamp <br>'
#print st

#print "<br><br>----------------XML CONFIG--------------------<br>"
for i in range(int(numKernel)):
	'''
	print '<br><br>KERNEL ',i 
	print '<br>Argv   : ',form.getvalue('argv'+str(i));
	print '<br>Global : ',form.getvalue('global'+str(i));
	print '<br>Local  : ',form.getvalue('local'+str(i));
	print '<br>Res    : ',form.getvalue('result'+str(i));
	print '<br>Type   : ',form.getvalue('type'+str(i));
	'''
	argv = str(form.getvalue('argv'+str(i)))
	res = str(form.getvalue('result'+str(i)))
	local_dim = str(form.getvalue('local'+str(i)))
	global_dim = str(form.getvalue('global'+str(i)))

	
	xml_str = """<kernel>
<output_dim>%s</output_dim>
<arguments>%s</arguments>
<global_work_size>%s</global_work_size>
<local_work_size>%s</local_work_size>
</kernel>
	""" %(res,argv,global_dim,local_dim)

	open(save_path+'/xml/'+str(i)+'.xml','w').write(xml_str)
	



#print "<br><br>----------------KERNEL CODE--------------------<br>"



kernel_code = ""
kernel_code = kernel_code + "from sparkcl import SparkCLContext ,SparkCLKernel , SparkCL\n"
kernel_code = kernel_code + 'if __name__ == "__main__" : \n'
kernel_code = kernel_code + '\t' + 'work_path = "' + save_path + '"\n'
kernel_code = kernel_code  + '\t' + 's_cl = SparkCL("%s","%s")\n' %(app_name,os.environ["SERVER_NAME"].strip())
code_path = os.environ['SPARKCL_HOME']+"/lib/network/cgi-bin/kernelList_file"


for i in range(int(numKernel)):
	copyfile(code_path+"/"+form.getvalue('kernel_id_'+str(i)),save_path+'/kernel/'+str(i)+'.cl')
	kernel_code = kernel_code + '\t' + 'kernel%s = SparkCLKernel("%s",work_path+"/kernel/%s.cl",work_path+"/xml/%s.xml",output_type="int")\n'%(str(i),'kernel'+str(i),i,i)
	kernel_code = kernel_code + '\t' + 's_cl.addKernel(kernel%s,type="%s")\n'%(i,form.getvalue('type'+str(i)))

kernel_code = kernel_code + '\t' + 'data = ['+file_data.replace('\n','')+']\n'
kernel_code = kernel_code + '\t' + 'print s_cl.run(data)'

open(save_path+'/sparkcl_code.py','w').write(kernel_code)

#print kernel_code.replace('\n','<br>')

#print '<br><br>Save to <br>'
#print  save_path + str(st)+'.py'
#open(save_path + str(st)+'.py','w').write(kernel_code)

getNohupID = subprocess.Popen(["nohup %s %s > /dev/null 2>&1 & echo $!" %(os.environ["SPARKCL_HOME"]+"/bin/sparkcl-submit.sh",save_path+'/sparkcl_code.py')], stdout=subprocess.PIPE, shell=True)
(nohupID, err) = getNohupID.communicate()
#print nohupID
#time.sleep(3)

print """<html>
<head>

<link href="bootstrap-3.3.2-dist/css/blinker.css" rel="stylesheet">
<meta http-equiv="refresh" content="6; url=/index.py" />
</head>
<body>
<b class='blink_me'>Preparing</b>
</body>
</html>"""

