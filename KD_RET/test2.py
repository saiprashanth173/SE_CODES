#!usr/bin/python
import gla
import stats
import special
import retriv1
import cgi
#print "Content-type:text/html\r\n\r\n"
def get(query):
	orig_query = query
	query = gla.gaiml(query)
	#print query
	#print "#------------------------AIML------------------#"
	#print query
	ans = gla.compute(query[0])
	#print ans
	if ans=="<NA>":
		for i in query:
			query = gla.gdisc(i)
			#print query
			#print "#------------------------DISC------------------#"
			#print "Rest :",query
			msg = gla.gspl(orig_query)
		
			#print [msg]
			if msg!="":
				#print "here"
				#print "#------------------------SPL-------------------#"
				ans = special.getanswer(msg,query,orig_query)
				#return ans
				#print msg,":",ans
			else:
				query,cols = gla.wordmatrix(query)
				#print "#-----------------------WM---------------------#"
				#print "Rest :",query
				#print "Fields :",cols
				#print "#-----------------------TAB---------------------#"
				#tabs = gla.gettable(query,cols)
				#print "Tables :",tabs
				#print "#----------------------STATS--------------------#"
				#flag,field,table = gla.getstats(query)
				#if flag:
					#ans = stats.grapher(table,field)
				#else:
					#print ""
				#print "#-----------------------LOG---------------------#"
				query,symbol,wtn,date = gla.logic(query)
				#print wtn	
				#print "Rest :",query
				#print "Symbol :",symbol
				#print "Values :",wtn
				#print "Date :",date
				#print "#---------------------RETRIV--------------------#"
				#print query
	
				ans = retriv1.getanswer(query,symbol,wtn,date)
				ans[0]={"general":ans[0]}
				#print "Ans :",ans		
			#print "#---------------------END----------------------#" 
		#print ans
		return ans
