#coding=utf-8
import re,urllib,sys,MySQLdb as mdb
import chardet

reload(sys)
#sys.setdefaultencoding('utf-8')
#s='#NAME?' #������raw_input()����Ҳ��
def	geturl():
	#db =mdb.connect(host='127.0.0.1',user='root',passwd='hehe',db='public_opinion',charset='utf8')
	#cur=db.cursor()
	s=raw_input("������ؼ���:")
	s=s.decode(sys.stdin.encoding).encode('utf-8')
	
	#print chardet.detect(s)
	#query='insert into key_word (keyword) values("'+s+'")'
	#print query
	#cur.execute(query)

	#db.commit()
	#cur.close()

	#s_utf=s.decode(sys.stdin.encoding).encode('utf-8')  #������Ҫת��Ϊutf-8
	
	return urllib.quote(s)
'''
if __name__=='__main__':
	geturl()
'''
