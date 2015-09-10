#coding=utf-8
from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint
from sgmllib import SGMLParser
from bs4 import BeautifulSoup
import time,math
# import MySQLdb as mdb
import re,chardet,sys
import os
import setting
reload(sys)
sys.setdefaultencoding('utf8')
#######################################

#################################################
user_url='http://weibo.com/iamfeihong'
os.system('python C:\\Users\\MINUS\\Desktop\\work\\weibo_reaseach\\user_homepage.py %s' % user_url)
time.sleep(5)