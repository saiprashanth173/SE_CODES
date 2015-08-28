

def removePandS(content):
    import re,string
    re.sub(r'\b\w{,2}\b',' ', content)
    re.sub(r'\b\w{15,}\b',' ', content)
    regex=re.compile('[%s]'% re.escape(string.punctuation))
    content=re.sub(regex," ",content)
    return content.split()


def getData(query):
    import mainRetrieveCount as mr
    query=query.lower()
    query = removePandS(query)
  #  print query
    ids =mr.getListQuery(query)
    #print ids
    content = fetchResults(ids[:10])
   # print content

def fetchResults(ids,db,table):
    import MySQLdb

    db = MySQLdb.connect('127.0.0.1','root','#srmseONserver1',db)

    cursor= db.cursor(MySQLdb.cursors.DictCursor)
    values=str(tuple(ids)).replace("u","")
    values=values.replace(',)',')')#if len of tuple is 1 then ('101568',)
    #print values
    if table == "main_links":
        sql="SELECT `link` as `url`,SUBSTR(`title`,1,100) as `title`,SUBSTR(`description`,1,200) as `body`,`img_link` as `img` FROM %s WHERE `id` IN %s ORDER BY FIELD(`id`,%s) "%(table,values,values[1:len(values)-1])
    else:        
        sql="SELECT `url`,SUBSTR(`title`,1,100) as `title`,SUBSTR(`body`,1,200) as `body` FROM %s WHERE `id` IN %s ORDER BY FIELD(`id`,%s) "%(table,values,values[1:len(values)-1])
 #   sql = "SELECT `url`,`title` FROM source_main WHERE `id` IN %s ORDER BY alexa desc"%(values)
    #print sql
    cursor.execute(sql)

    data = cursor.fetchall()
    #print data

    return list(eval(str(data).replace('\\x',' ')))
def fetchDescWiki(title):
	import MySQLdb
	# Open database connection
	db = MySQLdb.connect("localhost","root","#srmseONserver1","wiki" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# Prepare SQL query to INSERT a record into the database.
	sql = """SELECT `desc`,`infobox` FROM description WHERE `title`='%s'"""%(title)
	try:
	   # Execute the SQL command
	   cursor.execute(sql)
	   results=cursor.fetchone()
	   if not results is None:
	   	return results
	   else:
	   	return ["",""]
	   db.commit()
	   db.close()
	   # Commit your changes in the database
	   
	except Exception as e:
	   #print e
	   return title,""
	   # Rollback in case there is any error
	   db.rollback()

	# disconnect from server
	db.close()
def fetchResultsWiki(ids,db,table,query):
	import json
	#ids are actually titles now
	lii=[]
	d={}
	d["title"]=ids[0]
	h=fetchDescWiki(ids[0])
	#d["body"],d["infobox"]=fetchDescWiki(i)
	d["body"]=str(filter(lambda x:ord(x)>31 and ord(x)<128,h[0]))
	d["infobox"]=str(filter(lambda x:ord(x)>31 and ord(x)<128,h[1]))
	#print d
	lii.append(d)
	return lii

#    import MySQLdb
#    def changeIds(i):
#	return i[3:]

#    db = MySQLdb.connect('127.0.0.1','root','#srmseONserver1',db)
#    ids = map(changeIds,ids)
#    cursor= db.cursor(MySQLdb.cursors.DictCursor)
#    values=str(tuple(ids)).replace("u","")
#    values=values.replace(',)',')')#if len of tuple is 1 then ('101568',)
#    sql="SELECT SUBSTR(page.page_title,1,100) as `title`,SUBSTR(CAST(text.old_text AS CHAR),800,400) AS `body` FROM %s INNER JOIN text ON text.old_id = page.page_id WHERE page.page_id IN %s ORDER BY FIELD(page.page_id,%s) "%(table,values,values[1:len(values)-1])
 #   sql = "SELECT `url`,`title` FROM source_main WHERE `id` IN %s ORDER BY alexa desc"%(values)
#    #print sql
#    cursor.execute(sql)
#
#    data = cursor.fetchall()
#
#    return list(eval(str(data).replace('\\x',' ')))

#query=raw_input()

#getData(query)
