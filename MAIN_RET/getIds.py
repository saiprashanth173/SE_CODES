#!/usr/bin/python
from threading import Thread as T
import threading,json
from Queue import Queue
import mainGla as MG
import mainRetrieve as MR
import cgi,cgitb,json
form = cgi.FieldStorage()
cgitb.enable()
query = form.getvalue('q','###123###')
f = form.getvalue('f','###123###')
print "Content-type:text/html\r\n\r"
import decryptCSRF as csrf
res={}
token=form.getvalue('authenticity_token','###123###')
import askMeAsync as ask
if query!="###123###" and f!="###123###" and token!="###123###" and csrf.decrypt(token):
      dic=ask.getQuery(query,f)
      s=json.dumps(dic, ensure_ascii=True)
      print s
else:
	res["error"]="Unauthorized Access"
        print json.dumps(res)

#print "hii"
