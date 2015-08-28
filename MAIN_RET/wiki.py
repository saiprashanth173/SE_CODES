import nltk
from mergedict import MergeDict
from threading import Thread as Process
import MySQLdb,json,re,sys
th1=None#head processes
th2=None
stop = nltk.corpus.stopwords.words('english')
wikiAns=[]
lis=[]
gotFromCache=False
wikiAnsGot=False
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
def addToCache(q,j):
	if not gotFromCache:
		import subprocess
		try:
			p=subprocess.Popen(["python","addToWikiCache.py"," ".join(q),j],shell=False)
		except Exception as e:
			#print e
			pass
def removeStopWords(data):
	"""Removes stop words"""
	return [i for i in data.split() if i not in stop]
def remove_punctuations(s):
	#This one does not remove the hash tags
	try:
		output = re.sub(r'[\'\.\,-\/!<>?$%\^&\*;:\+{}=\-_`~()\[\]]'," ", s)
		output = re.sub(r'\s+'," ", output).strip()
		return output.encode()
	except:
		return ""
def checkInCache(query):
	global wikiAns,wikiAnsGot,gotFromCache
	# Open database connection
	db = MySQLdb.connect("localhost","root","","wiki" )
	# prepare a cursor object using cursor() method
	cursor = db.cursor()
	# Prepare SQL query to INSERT a record into the database.
	q=query.lower().split()
	q.sort()
	query=" ".join(q)
	sql = """SELECT `title` FROM searchCache WHERE `query`='%s'"""%(query)
	try:
	   # Execute the SQL command
	   cursor.execute(sql)
	   results=cursor.fetchone()

	   if not results is None:
	   	 wikiAns=[results[0]]
	   	 gotFromCache=True
	   	 wikiAnsGot=True
		 return
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
def wikiMain(lis1):
    		global wikiAns,wikiAnsGot,check,lis
    		lis=lis1#copying the query words
	    	db = MySQLdb.connect("localhost","root","","wiki" )
	    	cursor = db.cursor()
	    	#print lis
	    	#length are used to check to support the string format of tuple as len 1 tuple is (key,) the comma creates problem with IN query in mysql
	    	if len(lis)>1:
	    		sql = """SELECT `word`,`json_data` from wordmatrix where word IN %s"""%(str(tuple(lis)))
	    	elif len(lis)==1:
	    		sql = """SELECT `word`,`json_data` from wordmatrix where word ='%s'"""%(str(lis[0]))
		try:
		   cursor.execute(sql)
		   db.commit()
		   res = cursor.fetchall()
		   listCounters=[]#initially holds all the the data of keys
		   listCounter=[]#holds the dics obtained from common keys
		   ke=set([])#stores common keys
		   first=True
		   loadedCache={}#stores loaded data from json.loads
		   for r in res:
		   	d=json.loads(r[1].replace("#dot#",".").lower())
		   	loadedCache[r[0]]=d
		   	if first:
		   		ke=set(d.keys())
		   		first=False
		   	else:
		   		ke=set(d.keys()).intersection(set(ke))
		   	listCounters.append(d)
		   if len(list(ke))==0:
		   	#print "got no common keys trying to remove stop words"
		   	words=removeStopWords(" ".join(lis))
		   	q=" ".join(words)
			global lis
			lis=words
			th2=Process(target=checkInCache,args=(q,))
			th2.start()
		   	listCounters=[]
		   	listCounter=[]
		   	ke=set([])#stores common keys
		   	first=True
		   	#Storing common keys in ke
		   	for r in res:
		   		if r[0] in words:
			   		d=loadedCache[r[0]]
			   		if first:
			   			ke=set(d.keys())
			   			first=False
			   		else:
			   			ke=set(d.keys()).intersection(set(ke))
		   			listCounters.append(d)
		   	if len(list(ke))==0:
		   		#Nothing found in removing stop words
		   		#Now do topic extraction
		   		tokens = nltk.word_tokenize(" ".join(lis))
				tagged = nltk.pos_tag(tokens)
				temp=[]
				for t in tagged:
					if t[1][0]=="N":
						temp.append(t[0])
		   		q=" ".join(temp)
				global lis
				lis=temp
				th2=Process(target=checkInCache,args=(q,))
				th2.start()
		   		listCounters=[]
		   		listCounter=[]
		   		ke=set([])#stores common keys
		   		first=True
		   		#Storing common keys in ke
		   		for r in res:
		   			if r[0] in temp:
			   			d=loadedCache[r[0]]
			   			if first:
			   				ke=set(d.keys())
			   				first=False
			   			else:
			   				ke=set(d.keys()).intersection(set(ke))
		   				listCounters.append(d)
		   		if len(list(ke))==0:
		   			#finally no ans
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
		    	global sor
		   	sor=sorted(result, key=result.get, reverse=True)
		   	#if we already have 1 for 1 keyword and title is 2 keyword
		   	#ex sachin tendulkar we got Sachin:1 but not right results
		   	#right on is Sachin:0s.5 Tendulkar:0.5
		   	#below for loop for doing exact match
		   	#print sor
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
					return				
		   		elif t.lower()=="_".join(lis):
					#Not a redirect but a exact match
			   		sor[ind],sor[0]=sor[0],sor[ind]
			   		b=checkForDis(sor)
					wikiAns=[b]
					wikiAnsGot=True
					return
			#did'nt got exact match just return 1
			#Exact match with user query not found but found something which adds upto 1
		   	if result[sor[0]]==1.0:
		   		if "#r#" in sor[0]:
		   			resolved=resolveRedirects(sor[0].replace("#r#",""))
			   		sor[0]=resolved
		   			wikiAns=[sor[0]]
		   			wikiAnsGot=True
					return
		   		else:
		   			b=checkForDis(sor)
		   			wikiAns=[b]
		   			wikiAnsGot=True
		   			return
			else:
		   		rnks=compareRanks(sor)
		   		if not len(rnks)==0:
		   			if "#r#" in rnks[0]:
		   				wikiAns=[resolveRedirects(rnks[0].replace("#r#",""))]
		   				wikiAnsGot=True
		   				return
					else:
		   				wikiAns=[rnks[0]]
		   				wikiAnsGot=True
						return
		   		else:
		   			if "#r#" in sor[0]:
		   				wikiAns=[resolveRedirects(sor[0].replace("#r#",""))]
		   				wikiAnsGot=True
						return
		   			else:
		   				b=checkForDis(sor)
		   				wikiAns=[b]#worst result not exact match not ranked
		   				wikiAnsGot=True
						return
		   else:
		   	wikiAns=[]
		   	wikiAnsGot=True
			return
		except Exception as e:
		   typee, value, traceback = sys.exc_info()
    		   #print typee
		   # Rollback in case there is any error
		   db.rollback()
		   wikiAns=[]
		   wikiAnsGot=True
		   return

		# disconnect from server
		db.close()
def waitForAns():
	global wikiAnsGot,lis
	while not wikiAnsGot:
		pass
	if len(wikiAns)==0:
		pass
	else:
		addToCache(lis,wikiAns[0])
def main(wiki_query):
	global th1,th2
	q=" ".join(wiki_query)#passing org query
	th1=Process(target=checkInCache,args=(q,))
	th1.start()
	th2=Process(target=wikiMain,args=(wiki_query,))
	th2.start()
	tt=Process(target=waitForAns,args=())
	tt.start()
	tt.join()
	return wikiAns
