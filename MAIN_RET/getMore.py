#!/usr/bin/python
import getMoreResults as GMR
import decryptCSRF as csrf
import cgi,cgitb,json
form = cgi.FieldStorage()
cgitb.enable()
ids = form.getvalue('q','###123###')
f = form.getvalue('f','###123###')
res={}
token=form.getvalue('authenticity_token','###123###')
print "Content-type:text/javascript\r\n\r"
import askMeAsync as ask
if ids!="###123###" and f!="###123###" and token!="###123###" and csrf.decrypt(token):
   ids =ids.split(",")
   print json.dumps(GMR.getResults(ids,f))
else:
   res["error"]="Unauthorized Access"
   print json.dumps(res)
