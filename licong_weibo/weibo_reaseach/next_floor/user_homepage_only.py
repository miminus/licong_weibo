#coding=utf-8
import time
import sys
import MySQLdb as mdb
import os,chardet
from selenium import webdriver
import urllib2,re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import math,setting
print 'start'

#################################################
db = mdb.connect(host=setting.DB_HOST,user=setting.DB_USER,passwd=setting.DB_PASSWD,db=setting.DB_DATABASE,charset="utf8" )
cur=db.cursor()
###############################################

follower_list_str=sys.argv[1]
follower_list=follower_list_str.split(',')
#f=open('C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\next_floor\\user_main.txt','wb')
#homepage=sys.argv[1]
#homepage='http://weibo.com/u/'+homepage
#homepage='http://weibo.com/kaifulee'
count=0
reload(sys) 
sys.setdefaultencoding('utf8')
driver=webdriver.Ie()
driver.get('http://www.weibo.com')
time.sleep(2)
for homepage in follower_list:
	if len(homepage)>30:
		continue
#WebDriverWait(driver, 10)..until(EC.presence_of_element_located((By.ID,'someid')))
	while True:
		try:
			#driver.implicitly_wait(10)
			print 'go in'
			print 'only_user_homepage'
			homepage=homepage.replace('\'','')
			if int(count)%5==0:
				driver.get('http://www.weibo.com')
				time.sleep(4)
			print homepage
			driver.get(homepage)
			time.sleep(2)
			element = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"plc_main")))
			#print element
			# try:
			flag=0
			main_area=driver.find_element_by_id('plc_main')
			head_area=driver.find_element_by_class_name('photo_wrap')
			gender_area=driver.find_element_by_class_name('pf_username')  
			try:
				person_message_area=driver.find_element_by_class_name('ul_detail')
			except:
				pass
			user_area=driver.find_element_by_xpath('//div[@node-type="focusLink"]')
			# driver.execute_script('window.scrollBy(0,document.body.scrollHeight)','')
			print 'inner_only user_homepage'
			# except:
				# main_area=driver.find_element_by_class_name('PRF_profile_header')
				# flag=1
			break
		except:
			driver.quit()
			time.sleep(3)
			driver=webdriver.Ie()
			driver.get('http://www.weibo.com')
			continue
			
	count=count+1
	content=main_area.get_attribute('outerHTML')
	head=head_area.get_attribute('outerHTML')
	gender=gender_area.get_attribute('innerHTML')
	# person_message=person_message_area.get_attribute('innerHTML')
	user_message=user_area.get_attribute('outerHTML')

	content=content.encode('utf-8')
	head=head.encode('utf-8')
	gender=gender.encode('utf-8')
	# per_mess=person_message.encode('utf-8')
	user_message=user_message.encode('utf-8')


	soup=BeautifulSoup(content)
	# f=open('d:/aa.txt','wb')
	# f.write(content)
	# f.close()
	if flag==0:
		#f.write(soup.prettify())
		#f.close()
		content=soup.prettify()
		#############解析开始#########################
		uid_pattern=re.compile('src="http://.*?sinaimg.cn/(\d+)/',re.S)
		user_pattern=re.compile('alt=(.*?)src')
		user_image_pattern=re.compile('src="(http://.*?)"',re.S)
		user_pattern=re.compile('uid=(\d+)&.*?fnick=(.*?)&',re.S)
		
		per_mess_pattern=re.compile(r'<span class="item_text W_fl">.*?</li>',re.S)
		sub_p_1 = re.compile('<[^<>]*?>|\r', re.S)	
		class_pattern=re.compile(r'Lv.(\d+)',re.I)
		digit_pattern=re.compile(r'>\s*(\d+)\s*<',re.S)
		#aa='(\d+)\s*<.*?>\s*<.*?>\s*关注'.decode('gbk').encode('utf-8')
		#followee_pattern=re.compile(aa,re.S)
		#follower_pattern=re.compile(r'(\d+)\s*<.*?>\s*<.*?>\s*粉丝',re.S)
		#postnum_pattern=re.compile(r'(\d+)\s*<.*?>\s*<.*?>\s*微博',re.S)
		#################################################################
		user=re.findall(user_pattern,user_message)[0]
		uid = user[0]
		user= user[1]
		try:
			user_image=re.findall(user_image_pattern,head)[0]
		except:
			user_image=''
		#print user_image
		if 'female' in gender:
			gender_sex='female'
		else:
			gender_sex='male'
		#print gender_sex
		
		per_message=re.findall(per_mess_pattern,content)
		message=''
		for m in per_message:
			m= m.replace('\n','')
			m= m.replace(' ','')
			m= re.sub(sub_p_1,' ',m)  
			
			message+=m
		#print message
		strongs=soup.find_all('strong')
		dig=[]
		
		for i in strongs:
			try:
				a=re.findall(digit_pattern,str(i))[0]
				print a
				dig.append(a)
			except:
				pass
		try:
			followee_num=dig[0]
			follower_num=dig[1]
			posts_num=dig[2]
		except:
			followee_num=0
			follower_num=0
			posts_num=0
		try:
			_class=re.findall(class_pattern,content)[0]
		except:
			_class=''
			pass
		print _class
	##########################################################
	##########################################################
	##########################################################
	key_wd_id='1'
	query='insert ignore into weibo_user (user_id,user_name,user_image,gender,message,class,post_num,follower_num,followee_num,key_wd_id) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
	params=(uid,user,user_image,gender_sex,message,_class,posts_num,follower_num,followee_num,key_wd_id)			
	cur.execute(query,params)
	db.commit()
	time.sleep(5)
driver.quit()
#####################访问关注与粉丝#############################
# follower_url='http://weibo.com/'+uid+'/fans?page='
# followee_url='http://weibo.com/'+uid+'/follow?page='

# follower_page=int(math.ceil(float(int(follower_num)/20.0)))
# followee_page=int(math.ceil(float(int(followee_num)/20.0)))

# if follower_page>5:
	# follower_page=5
# if followee_page>5:
	# followee_page=5
# if posts_num>100:
	# post_page=3
# else:
	# post_page=int(math.ceil(float(int(posts_num)/45.0)))
	
# os.system('python C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\next_floor\\follower.py %s %d %s %s' %(follower_url,follower_page,uid,user))
# time.sleep(4)
# os.system('python C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\next_floor\\followee.py %s %d %s %s' %(followee_url,followee_page,uid,user))
# time.sleep(4)
# os.system('python C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\next_floor\\userpost.py %s %d' % (uid,post_page))
# time.sleep(4)
###################################################















