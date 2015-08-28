import mongoRetrivChange3 as rv
from threading import Thread
def getanswer(query,symbol,wtn,date):
        ans = "<NA>"
	ans=rv.queryRetriv(query)
	return ans
