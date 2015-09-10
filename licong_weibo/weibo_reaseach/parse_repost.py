#coding=utf-8
import re,sys
import MySQLdb as mdb
import time,setting

#################################################
db = mdb.connect(host=setting.DB_HOST,user=setting.DB_USER,passwd=setting.DB_PASSWD,db=setting.DB_DATABASE,charset="utf8" )
cur=db.cursor()
###############################################

f=open(r'%s/page_repost.txt' % setting.CURRENT_PATH,'rb')
page_content=f.read()
f.close()

content_pattern=re.compile(r'(feed_list_item.*?feed_list_item_date.*?</div>)',re.S)
post_id_pattern=re.compile(r'rootmid=(\d+)',re.S)
repost_id_pattern=re.compile(r';mid=(\d+)',re.S)
commenter_pattern=re.compile(r'<img alt=.{0,1}"(.*?)"',re.S)
commenter_homepage_pattern=re.compile(r'href=.{0,1}\"(.*?)\"',re.S)
commenter_id_pattern=re.compile(r'id=(\d+)',re.S)
repostion_pattern=re.compile(r'wb_text".{0,1}>(.*?)</div>',re.S)
reposter_image_pattern=re.compile(r'<img.*?src=.{0,1}\"(.*?)\"',re.S)

sub_p_1 = re.compile('<[^<>]*?>|\r', re.S)
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
    ustr = str
    return ustr

content=re.findall(content_pattern,page_content)
print len(content)
for i,d in enumerate(content):
    scratch_time=time.strftime('%Y-%m-%d %H:%M:%S')
    # print scratch_time
    #########################################
    repost_id=re.findall(repost_id_pattern,d)[0]
    print repost_id
    ##########################################
    post_id=re.findall(post_id_pattern,d)[0]
    # print post_id
    #########################################
    reposter_image=re.findall(reposter_image_pattern,d)[0]
    # print reposter_image
    #########################################
    repostter=re.findall(commenter_pattern,d)[0]
    #commenter=commenter.replace('\'','')

    #print commenter.decode('utf-8').encode('gbk')
    #########################################
    commenter_homepage=re.findall(commenter_homepage_pattern,d)[0]
    commenter_homepage='http://www.weibo.com'+commenter_homepage
    #print commenter_homepage
    ########################################
    reposter_id=re.findall(commenter_id_pattern,d)[0]
    print reposter_id
    ########################################
    repostion=re.findall(repostion_pattern,d)
    repostion=map(lambda x:parse_html_content(x),repostion)[0]
    #print commention
    ##########################################

    query='insert ignore into repost (repost_id,reposter_id,reposter,reposter_image,repost_content,post_id,scratch_time) values(%s,%s,%s,%s,%s,%s,%s)'
    params=(repost_id,reposter_id,repostter,reposter_image,repostion,post_id,scratch_time)

    cur.execute(query,params)
    db.commit()

    print '+++++++++++++++++++++++++'
cur.close()