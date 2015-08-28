from pymongo import MongoClient as mc
from mergedict import MergeDict
from threading import Thread as Process
import MySQLdb,json,re
wikiAns=[]
wikiAnsGot=False
def remove_punctuations(s):
	#This one does not remove the hash tags
	try:
		output = re.sub(r'[\'\.\,-\/!<>?$%\^&\*;:\+{}=\-_`~()\[\]]'," ", s)
		output = re.sub(r'\s+'," ", output).strip()
		return output.encode()
	except:
		return ""
def checkInCache(query):
	global wikiAns,wikiAnsGot
	# Open database connection
	db = MySQLdb.connect("localhost","root","","wiki" )
	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	# Prepare SQL query to INSERT a record into the database.
	sql = """SELECT `title` FROM searchCache WHERE `query`='%s'"""%(query)
	try:
	   # Execute the SQL command
	   cursor.execute(sql)
	   results=cursor.fetchone()

	   if not results is None:
	   	 wikiAns=[results[0]]+["CACHE"]
	   	 wikiAnsGot=True
	   # Commit your changes in the database
	   db.commit()
	except Exception as e:
	   #print e
	   # Rollback in case there is any error
	   db.rollback()
	# disconnect from server
	db.close()
def checkForDis(s):
	if s[0]+"_(disambiguation)" in s:
		
		return giveTopPageDisambiguation(s[0]+"_(disambiguation)")
	elif "#r#"+s[0]+"_(disambiguation)" in s:#if redirect disambiguation
		return giveTopPageDisambiguation(s[0]+"_(disambiguation)")
	else:
		return s[0]
def giveTopPageDisambiguation(s):
	# Open database connection
	db = MySQLdb.connect("localhost","root","","wiki" )
	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	# Prepare SQL query to INSERT a record into the database.
	sql = """SELECT `best`,`real` FROM disambiguationResolver WHERE `title`='%s'"""%(s)
	try:
	   # Execute the SQL command
	   cursor.execute(sql)
	   results=cursor.fetchone()
	   if results[1]==1:
	   	return results[0]
	   else:
	   	return s.replace("_(disambiguation)","")
	   # Commit your changes in the database
	   db.commit()
	except Exception as e:
	   #print e
	   return s
	   # Rollback in case there is any error
	   db.rollback()
	# disconnect from server
	db.close()
	return s
def resolveRedirects(s):
	global sor
	if "(disambiguation)" in s:#resolving disambiguations
		return giveTopPageDisambiguation(s)
	else:
		# Open database connection
		db = MySQLdb.connect("localhost","root","","wiki" )

		# prepare a cursor object using cursor() method
		cursor = db.cursor()

		# Prepare SQL query to INSERT a record into the database.
		sql = """SELECT `to` FROM redirectResolver WHERE `from`='%s'"""%(s)
		try:
		   # Execute the SQL command
		   cursor.execute(sql)
		   results=cursor.fetchone()
		   return checkForDis([results[0]]+sor)
		   # Commit your changes in the database
		   db.commit()
		except Exception as e:
		   #print e
		   return checkForDis([s]+sor)
		   # Rollback in case there is any error
		   db.rollback()

		# disconnect from server
		db.close()
		return s
class SumDict(MergeDict):
    @MergeDict.dispatch(int)
    def merge_int(this, other):
        return this + other
class SumDict1(MergeDict):
    @MergeDict.dispatch(float)
    def merge_int(this, other):
        return this + other 
def compareRanks(l):
	# Open database connection
	db = MySQLdb.connect("localhost","root","","wiki" )

	# prepare a cursor object using cursor() method
	cursor = db.cursor()

	# Prepare SQL query to INSERT a record into the database.
	sql=""
	if len(l)>1:
		ll=[]
		for n in l:
			try:
				nn=n.replace("#r#","").encode()
				ll.append(MySQLdb.escape_string(nn))
			except:
				pass
		if len(ll)==1:
			sql = "SELECT title,pv FROM rank WHERE title='%s' ORDER by pv"%(ll[0])
		else:
			sql = "SELECT title,pv FROM rank WHERE title IN %s ORDER by pv"%(str(tuple(ll)).replace("u'","'"))
	elif len(l)==1:
		sql = "SELECT title,pv FROM rank WHERE title='%s' ORDER by pv"%(MySQLdb.escape_string(l[0]))
	else:
		return []
	try:
	   # Execute the SQL command
	   cursor.execute(sql)
	   results=cursor.fetchall()
	   res=[]
	   never_visited=[]
	   for r in results:
	   	if r[1]==0:
	   		never_visited.append(r[0])
	   	else:
	   		res.append(r[0])
	   res=res+never_visited
	   # Commit your changes in the database
	   db.commit()
	   return res
	except Exception as e:
	   #print e
	   # Rollback in case there is any error
	   db.rollback()

	# disconnect from server
	db.close()
def getListQuery(lis,dbase,coll):
    from pymongo import MongoClient as mc
    from collections import Counter
    check = 0
    client = mc()
    if dbase == "testIndex":
        client = mc("192.168.103.25")
    if dbase=="wiki":
    	def wikiMain():
    		global wikiAns,wikiAnsGot,check
	    	db = MySQLdb.connect("localhost","root","","wiki" )
	    	cursor = db.cursor()
	    	#print lis
	    	if len(lis)>1:
	    		sql = """SELECT json_data from wordmatrix where word IN %s"""%(str(tuple(lis)))
	    	elif len(lis)==1:
	    		sql = """SELECT json_data from wordmatrix where word ='%s'"""%(str(lis[0]))
		try:
		   # Execute the SQL command
		   cursor.execute(sql)
		   #print sql
		   # Commit your changes in the database
		   db.commit()
		   res = cursor.fetchall()
		   listCounters=[]
		   listCounter=[]
		   ke=set([])#stores common keys
		   first=True
		   #Storing common keys in ke
		   for r in res:
		   	d=json.loads(r[0].replace("#dot#","."))
		   	#print d
		   	if first:
		   		ke=set(d.keys())
		   		first=False
		   	else:
		   		ke=set(d.keys()).intersection(set(ke))
		   	listCounters.append(d)
		   	if len(list(ke))==0:
		   		wikiAns=[]#no results got
		   		wikiAnsGot=True
		   for l in listCounters:
		   	d={}#creating dict from common keys
		   	for k in list(ke):
		   		d[k]=l[k]
		   	listCounter.append(d)
		   check =1#no idea why prashant used this
		   result=SumDict1({})#Sum of dicts in listCounters will be stored here
		   if check ==1:
			for li in listCounter:
				result.merge(li)
		    	#print result
		    	global sor
		   	sor=sorted(result, key=result.get, reverse=True)
		   	#if we already have 1 for 1 keyword and title is 2 keyword
		   	#ex sachin tendulkar we got Sachin:1 but not right results
		   	#right on is Sachin:0s.5 Tendulkar:0.5
		   	#below for loop for doing exact match
		   	
		   	for ind,term in enumerate(sor):
		   		#remove punctuataion ex ajay k. sood vs ajay k sood
		   		t=term.lower()#remove_punctuations(term)# this does not remove hash tags
		   		redirect=False
		   		if "#r#" in t and t.replace("#r#","")=="_".join(lis):
		   			#This condition is for checking if user query matches to a redirect page
	       		   		resolved=resolveRedirects(term.replace("#r#",""))
			   		sor[ind],sor[0]=sor[0],resolved
					wikiAns=[sor[0]]  
					wikiAnsGot=True  
					break				
		   		elif t.lower()=="_".join(lis):
					#Not a redirect but a exact match
			   		sor[ind],sor[0]=sor[0],sor[ind]
			   		b=checkForDis(sor)
					wikiAns=[b]
					wikiAnsGot=True
					break
			#did'nt got exact match just return 1
			#Exact match with user query not found but found something which adds upto 1
		   	if result[sor[0]]==1.0:
		   		#print result[sor[0]]
		   		if "#r#" in sor[0]:
		   			resolved=resolveRedirects(sor[0].replace("#r#",""))
			   		sor[0]=resolved
		   			wikiAns=[sor[0]]
		   			wikiAnsGot=True
		   		else:
		   			b=checkForDis(sor)
		   			wikiAns=[b]
		   			wikiAnsGot=True
		   	else:
		   		rnks=compareRanks(sor)
		   		if not len(rnks)==0:
		   			if "#r#" in rnks[0]:
		   				wikiAns=[resolveRedirects(rnks[0].replace("#r#",""))]
		   				wikiAnsGot=True
		   			else:
		   				wikiAns=[rnks[0]]
		   				wikiAnsGot=True
		   		else:
		   			if "#r#" in sor[0]:
		   				wikiAns=[resolveRedirects(sor[0].replace("#r#",""))]
		   				wikiAnsGot=True
		   			else:
		   				b=checkForDis(sor)
		   				wikiAns=[b]#worst result not exact match not ranked
		   				wikiAnsGot=True
		   else:
		   	wikiAns=[]
		   	wikiAnsGot=True
		except Exception as e:
		   #print e
		   # Rollback in case there is any error
		   db.rollback()

		# disconnect from server
		db.close()
	def waitForAns():
		global wikiAnsGot
		while not wikiAnsGot:
			pass
	q="".join(lis)
	th1=Process(target=checkInCache,args=(q,))
	th1.start()
	th2=Process(target=wikiMain,args=())
	th2.start()
	tt=Process(target=waitForAns,args=())
	tt.start()
	tt.join()
	return wikiAns
    #below portion is shared by both news and general
    db = client[dbase]
    results=db[coll].find({"keyword":{"$in":lis}},{"keyword":0,"_id":0})
    listCounters = list(results)
    if dbase  == "news" :
        #print len(listCounters),len(lis),lis
        if len(lis) == len(listCounters):
            #check =1
            #print list(getNewContent(listCounters))
            return list(getNewContent(listCounters))
    else:
        check =1
    
    result=SumDict({})
    if check ==1:
    
        for listCounter in listCounters:
            result.merge(listCounter)
    #print result
        sor=sorted(result, key=result.get, reverse=True)
        #print sor
        return sor
    else:
        return []


def getNewContent(contents):
    ids = []
    for content in contents:
        ids.append(set(content["ids"]))
    return set(ids[0]).intersection(*ids)


def remove(mongoDict):
    from collections import Counter

    mongoDict.pop('_id')
    mongoDict.pop('keyword')
    return mongoDict
    
