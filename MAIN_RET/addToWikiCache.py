#!/usr/bin/python
import sys,MySQLdb
def addToCache(q,j):
	try:
		db=MySQLdb.connect("localhost","root","#srmseONserver1","wiki")
        	cursor=db.cursor()
        	q=q.lower().split()
        	q.sort()
        	q1=" ".join(q)
        	#storing in cache in sorted fashion
        	sql="INSERT INTO `searchCache` (`query`,`title`) VALUES('%s','%s')"%(MySQLdb.escape_string(q1),MySQLdb.escape_string(j))
        	cursor.execute(sql)
		db.commit()
	except Exception as e:
		#print e
		db.rollback()
	db.close()
args=sys.argv
addToCache(args[1],args[2])
