#!/usr/bin/python
import MySQLdb,cgi,cgitb,json
form = cgi.FieldStorage()
cgitb.enable()
q = form.getvalue('q','###123###')
def fetchDB(x):
                if len(x)==0:
                    return []
                try:
		    table=""
		    num=str(x)[:3]
		    if num=="101":
			    table="source_main1"
		    elif num=="102":
			    table="source"
 		    elif num=="103":
			    table="source31"
                    elif num=="105":
                            table="source3"
 		    else:
			    return
 		    db = MySQLdb.connect("localhost","root","#srmseONserver","test" )
		    cursor = db.cursor()
		    sql = "SELECT `url` ,`title`,SUBSTR(`body`,0,200) FROM %s WHERE id='%s';" % (table,str(x))
		    cursor.execute(sql)
		    results = cursor.fetchall()
                    d={}
                    for r in results:
                        d["url"]=r[0]
                        d["title"]=r[1]
                        d["description"]=r[2]
                    db.close()
	            return d
		except:
		    print "Error: unable to fetCh data"
def main(arr):
    results=[]
    arr=arr.split(",")
    for a in arr:
        results.append(fetchDB(a))
    print "Content-type:text/javascript\r\n\r"
    print json.dumps(results)
main(q)
