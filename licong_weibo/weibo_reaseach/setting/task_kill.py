#coding=utf-8
import subprocess
import os
cmd='tasklist'
data=subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
i=0
cnt=0
a=data.stdout.readline()
while a:
	if i>4:
		c=a.split('.')
		name=c[0].strip()+'.exe'
		print name
	i+=1	
	a=data.stdout.readline().strip()