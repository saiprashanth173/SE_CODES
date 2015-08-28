
def getanswer(msg,query,orig_query):
	if msg == "<train status>":
		ans = train(query)
	elif msg == "<weather status>":
		ans = weather(query)
        elif msg == "<cricinfo module>":
                ans = cric_info(orig_query)
        elif msg == "<festival module>":
                ans = festival(orig_query)
        elif msg == "<tennis module>":
                ans = tennis(orig_query)
        elif msg == "<car module>":
        	ans=car(orig_query)
        elif msg == "<tank module>":
        	ans=tank(orig_query)
        elif msg == "<disease module>":
        	ans=disease(orig_query)       
	elif msg == "<flight module>":
                ans = flight(orig_query)
        elif msg == "<recipe module>":
                ans = recipe(orig_query)
	elif msg=="<discography module>":
		ans=discography(orig_query)
	elif msg=="<electronic module>":
		ans=electronic(orig_query)
        elif msg == "<wiki module>":
                ans = wiki_module(orig_query)

        elif msg == "<bank module>":
                ans = bank_module(orig_query)

	#elif msg == "<restaurant module>":
		#ans = restaurant(orig_query)
		
		
	#elif msg == "<website module>":
	#	ans = get_website(orig_query)

	elif msg == "<stock status>":
		ans = stock(query)
	elif msg == "<mineral status>":
		ans = mineral(query)
	elif msg == "<sports status>":
		ans = sports(query)
	elif msg == "<movie review>":
		ans = movie(query,orig_query)
        elif msg == "<exam status>":
                ans = exam(query)
        elif msg == "<locationcentric module>":
                ans = location(query)
	elif msg == "<highway module>":
                ans = highway(query)
	elif msg == "<differences module>":
                ans = differences(orig_query)
	elif msg == "<currency module>":
		ans = currency(query) 
	elif msg == "<meanings module>":
		ans= meanings(orig_query)  
        elif msg == "<theatre module>":
                ans= theatre(orig_query)
        elif msg == "<minister module>":
                ans= minister(orig_query)

        elif msg == "<std module>":
                ans= std(query)

        elif msg == "<bday module>":
                ans= [{"bday":[]}]

        elif msg == "<highcourt module>":
                ans = highcourt(orig_query)


	#print "here"             
	return ans

def festival(query):
	import festival_module as fm
	ans=fm.main(query)
	return ans

def flight(query):
        import flightmain as fm
        ans=fm.main(query)
        return ans
def tank(query):
	import tankretmain as trm
	ans=trm.main(query)
	return ans
def electronic(query):
	import electronicmain as em
	ans=em.main(query)
	return ans
def disease(query):
	import diseasemain as dm
	ans=dm.main(query)
	return ans
def car(query):
	import carretmain as cm
	ans=cm.main(query)
	return ans
def tennis(query):
	import tennismain as tm
	ans=tm.main(query)
	return ans
def recipe(query):
        import recipemain as rem
        ans=rem.main(query)
        return ans

def discography(query):
        import discoret as dt
        ans=dt.main(query,0)
        return ans
def highcourt(query):
	import highcourttest as hc
	ans = hc.main(query)
	return ans

#def restaurant(query):
#	import restaurantret as rret
#	ans = rret.resmain(query)
#	return ans
	
	
#def get_website(query):
#	import toptest as tst
#	ans = tst.main(query)
#	return ans

def std(query):
        ans = {}
        import stdmodule as st
        #print query
	ans = st.stdcodemod(query)
        #print ans
        if ans:
                return ans
        else:
                return [{}]



def wiki_module(query):
	ans ={}
	return [{"wiki":{}}] #flag to indicate no smart ans show infobox

def bank_module(query):
        ans ={}
        import bank_main as bm
        ans = bm.main(query)
        return ans

def cric_info(query):
        ans = {}
        import cricinfo as cric
        ans = cric.getQuery(query)
        #print ans
        if ans:
                return ans
        else:
                return [{}]


def minister(query):
        ans = {}
        import ministers as mr
        #print query
        ans = mr.main(query)
        #print ans
        if ans:
                return ans
        else:
                return [{}]



def theatre(query):
        ans = {}
        import theatreMain as th
        ans = th.theatre(query)
	#print ans
        if ans:
                return ans
        else:
                return [{}]


def meanings(query):
	ans = {}
	import meaning as mn
	ans = mn.main(query)
	if ans["dict"]:
		return [ans]
	else:
		return [{}]
	
def currency(query):
	ans = "<NA>"
	import currency
	ans = currency.get(query)
	return ans

def highway(query):
	ans = "<NA>"
	import highway1
	ans = highway1.highwaymod(query)
	return ans

def differences(query):
	import difference as dif
	ans = "<NA>"
	getAns= dif.difference(query)
	if getAns: 
		ans = [{"differences":getAns}]
	else:
		ans =[{}]
	return ans

def location(query):
        ans="<NA>"
        import locentric as location
        import restaurantret as restaur
        ans = location.main(query)
        res_result=restaur.resmain(query)
	if ans or res_result:
           
           #joining restaurant results of zomato and ixigo
           if "restaurants" in query or "restaurant" in query:
           	ans=[{"location":{"ixigo":ans,"zomato":res_result}}]
           else:
           	ans=[{"location":ans}]
	#print ans
	return ans



def exam(query):
        ans="<NA>"
        import exam
	
        ans = exam.main(query)
	#print ans
        if ans :
           ans=[{"exam":ans}]
        return ans


def movie(query,orig_query):
	ans="<NA>"
	import movieretrieve1 as mv
	ans = mv.new_movies(query)
	if ans :
	   ans[0]={"movie":ans[0]}
	#else:
	   #import movie_old
	   #ans = movie_old.movie(query,orig_query)
	return ans 
	
def train(query):
	ans = "<NA>"
        import train
        ans = list(train.main(query))
        #print ans
        if ans:
           ans={"train":ans}
        #print ans
	return [ans]

def weather(query):
        import weatherRetriv as wr
        
	ans = "<NA>"
	ans=wr.queryRetriv(query)
	#print ans
	if ans.has_key('time'):
		ans.pop('time')
	if ans.has_key('id'):
		ans.pop('id')
	
	
	return [{"weather":ans}]

def stock(query):
	import stockRetriv as sr
	ans = "<NA>"
	ans= sr.getResults(query)
	if ans:
	   ans[0]={"stock":ans[0]}
	return ans

def mineral(query):
	import GSOPA as gp
	ans = list(gp.main(query))
	#print "here"
	#print ans
	if ans:
		ans[0]={"minerals":ans[0]}
	return ans

def sports(query):
	ans = "<NA>"
	
	import score 
	
	ans= score.scoreRetriv(query)
	if ans:
	   ans[0]={"sports":ans[0]}
	return ans

