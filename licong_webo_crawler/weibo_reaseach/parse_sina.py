﻿#coding=utf-8
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from sgmllib import SGMLParser
from bs4 import BeautifulSoup
import time,math
import MySQLdb as mdb
import re,chardet,sys
import os
import setting
reload(sys)
import subprocess
sys.setdefaultencoding('utf8')
#######################################


#################################################
db = mdb.connect(host=setting.DB_HOST,user=setting.DB_USER,passwd=setting.DB_PASSWD,db=setting.DB_DATABASE,charset="utf8" )
cur=db.cursor()
###############################################





f=open('%s/posts.txt' % setting.CURRENT_PATH,'rb')
post_content=f.read()
f.close()

#post_content=post_content.decode('gb2312').encode('utf-8')
print chardet.detect(post_content)


post_con_pattern=re.compile(r'(<html>.*?</html>)',re.S)
title_pattern=re.compile(r'(<dl .*?action-type="feed_list_item".*?)\s*<dt',re.S)
post_id_pattern=re.compile(r'mid=\"\d+\"',re.S)
repost_url_pattern=re.compile(r'url=(.*?)&amp',re.S)
aa='title=\"(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\"'
digital_pattern=re.compile(r'(\d+)',re.S)
content_pp=re.compile(r'.*?：(.*?)',re.S)
post_url_pa=re.compile(r'class="W_textb" date.*?href="(http://weibo.com/.*?)" node-type="feed_list_item_date',re.S)
#aa=aa.decode('gb2312').encode('utf-8')
post_time_pattern=re.compile(aa,re.S)
inner_post_id_pattern=re.compile(r'omid=\"(\d+)\"',re.S)
inner_poster_url_pattern=re.compile(r'usercard=\"id=(\d+)\"',re.S)
sub_p_1 = re.compile('<[^<>]*?>|\r', re.S)

main_usr_pattern=re.compile(r'<div class="face">\s*<a href="(http://weibo.com.*?)"',re.S)
poster_pattern=re.compile(r'title="(.*?)"',re.S)
user_image_pattern=re.compile(r'src="(http://.*?)"',re.S)
user_id_pattern=re.compile(r'usercard="id=(\d+)',re.S)
def parse_html_content(str):
    '''return a unicode string'''
    str = re.sub(sub_p_1, '', str)    
    str = str.replace('&nbsp;', ' ')
    str = str.replace('&amp;', '')
    str = str.replace('#039;', '')
    str = str.replace('#', '')
    str = str.replace('&#160;', ' ')
    str = str.replace('&lt;', '<')
    str = str.replace('&gt;', '>')
    str = str.replace('&amp;', '&')
    str = str.replace('&quot;', '"')
    str = str.replace(' ','')
    str = str.replace('\n','')
    ustr = str
    return ustr
	
post_con=re.findall(post_con_pattern,post_content)
print "len: "+str(len(post_con))
if len(post_con)==0:
	sys.exit(0)

cnt=0
userlist=[]
for d in post_con:
	scratch_time = time.strftime('%Y-%m-%d %H:%M:%S')
	main_usr_url=re.findall(main_usr_pattern,d)[0]
	userlist.append(main_usr_url)
	#print main_usr_url
	main_poster=re.findall(poster_pattern,d)[0]
	#print main_poster
	user_image=re.findall(user_image_pattern,d)[0]
	#print user_image
	user_id=re.findall(user_id_pattern,d)[0]
	print user_id
	###############post_id######################
	post_id=re.findall(post_id_pattern,d)[0]
	post_id=re.findall(digital_pattern,post_id)[0]
	#print post_id
	soup= BeautifulSoup(d)
	#print soup.find(class="WB_text")
	#aa=soup.get_text()
	#######获取主文######################
	#aa=soup.find_all("div", "WB_text")
	aa=soup.find_all(attrs={'node-type':'feed_list_content'})
	aa=map(lambda x:parse_html_content(str(x)),aa)
	aa=aa[0]
	#print aa


	
	flag=0
	#################################
	#title=re.findall(title_pattern,d)[0]
	#print title
	#if 'omid' not in title:  #非转发
		#############转发########################
	try:	
		repost_num=soup.find_all(attrs={"action-type":"feed_list_forward"})
		repost_url_con=repost_num[0]
	except:
		repost_url=''
	
	try:
		repost_num=map(lambda x:parse_html_content(str(x)),repost_num)[0]
	except:
		pass
	try:
		repost_num=re.findall(digital_pattern,repost_num)[0]
	except:
		repost_num=0
	print 'repost_num:'+str(repost_num)
	########################post_url#################################
	post_url=re.findall(post_url_pa,d)
	post_url=post_url[len(post_url)-1]
	# print post_url
	'''
	#################转发url########################
	repost_url=re.findall(repost_url_pattern,str(repost_url_con))[0]
	print repost_url
	##############评论#######################
	'''
	comm_num=soup.find_all(attrs={"action-type":"feed_list_comment"})
	comm_num=map(lambda x:parse_html_content(str(x)),comm_num)[0]
	try:
		comm_num=re.findall(digital_pattern,comm_num)[0]
	except:
		comm_num=0
	print 'comm_num:'+str(comm_num)
	
	#############时间#######################
	post_time=soup.find_all("a",class_="W_textb")
	post_time=post_time[len(post_time)-1]
	#print post_time
	post_time=re.findall(post_time_pattern,str(post_time))[0]
	#print post_time
		#raw_input()
		
	'''
	#############有内贴#########################
	if 'omid' in title:
		flag=1
		print '+++++++'
		###############inner_post_id############
		inner_postid=re.findall(inner_post_id_pattern,d)[0]
		print inner_postid
		###############inner_poster——url##################
		inner_poster=soup.find_all(attrs={"node-type":"feed_list_originNick"})
		inner_post_con=inner_poster[0]
		inner_poster_url=inner_poster[0]['usercard']
		inner_poster_id=inner_poster_url[3:]
		print inner_poster_id
		###############homepage##################
		homepage=inner_poster[0]['href']
		homepage='http://weibo.com'+str(homepage)
		print homepage
		################inner_poster###############################
		inner_poster=map(lambda x:parse_html_content(str(x)),inner_poster)[0]
		print inner_poster
		##################poster_id##############
		#inner_poster_url=re.findall(inner_poster_url_pattern,str(inner_post_con))[0]
		#print inner_poster_url
		###############内部的帖子################
		inner_post=soup.find_all(attrs={"node-type":"feed_list_reason"})
		inner_post=map(lambda x:parse_html_content(str(x)),inner_post)[0]
		print str(inner_post)
		###############内部转发#################
		inner_repost=soup.find_all(attrs={"action-history":"rec=1"})
		#print len(inner_repost)
		inner_repost=map(lambda x:parse_html_content(str(x)),inner_repost)[0]
		inner_repost=re.findall(digital_pattern,inner_repost)[0]
		print str(inner_repost)
		##############内部评论#################
		inner_comm=soup.find_all("a",class_="S_func4")
		inner_comm=map(lambda x:parse_html_content(str(x)),inner_comm)[1]
		inner_comm=re.findall(digital_pattern,inner_comm)[0]
		print inner_comm
		#############内部时间##################
		inner_time=soup.find_all("a",class_="S_func2 WB_time")
		inner_time=inner_time[0]
		inner_time=re.findall(post_time_pattern,str(inner_time))[0]
		print inner_time
		query='insert ignore into post (post_id,poster,poster_id,poster_url,content,scratch_time,post_time,repost_num,comment_num) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)'
		params=(inner_postid,inner_poster,inner_poster_id,homepage,inner_post,scratch_time,inner_time,inner_repost,inner_comm)
		cur.execute(query,params)
		db.commit()
	'''
	query1='select post_id from post'
	cur.execute(query1)
	res=cur.fetchall()
	flag_cf=0
	for i in res:
		ress=i[0]
		if post_id == str(ress):
			flag_cf=1
	if flag_cf==1:
		continue
	#if '3635532662'==user_id:     #防止"创源晟汇-神算章"再出现
	#	continue
	key_wd_id='1'
	query="insert ignore into post (post_id,post_url,poster,poster_id,poster_url,image,content,scratch_time,post_time,repost_num,comment_num,key_wd_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	params=(post_id,post_url,main_poster,user_id,main_usr_url,user_image,aa,scratch_time,post_time,repost_num,comm_num,key_wd_id)
	cur.execute(query,params)
	'''
	if flag==1:
		cur.execute("UPDATE post SET repost_post_id=%s WHERE post_id=%s"%(str(inner_postid),str(post_id)))
	'''	
	db.commit()
	
    
    
    #####################################################################################
	if comm_num==0:
		comm_page=0
	else:
		comm_page=int(math.ceil(float(int(comm_num)/20.0)))
	comment_url='http://weibo.com/aj/comment/big?_wv=5&id='+post_id+'&page='
	# print comm_page
	if comm_page>10:
		comm_page=10

	

    ######################################################################################
	if repost_num==0:
		repost_page=0
	else:
		repost_page=int(math.ceil(float(int(repost_num)/20.0)))
	repost_url='http://weibo.com/aj/comment/big?_wv=5&id='+post_id+'&page='
	if repost_page>10:
		repost_page=10
        
	c1=None
	c2=None
	if comm_page!=0:
		c1=subprocess.Popen('python %s/repost.py %s %d' %(setting.CURRENT_PATH,post_id,comm_page))
	if repost_page!=0:
		c2=subprocess.Popen('python %s/real_repost.py %s %d' %(setting.CURRENT_PATH,post_id,repost_page))
	if c1!=None:
		c1.wait()
	if c2!=None:
		c2.wait()
    
    
	print '_+_+_+_+_+_new post+_+_+_+_+_+_+'    
print cnt


