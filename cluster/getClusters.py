#!/usr/bin/python 
import cgi,cgitb,json
import decryptCSRF as csrf
import clusterRetrieval as CR
#cgitb.enable()
print "Content-type:text/javascript\r\n\r"
res={}
form = cgi.FieldStorage()
token=form.getvalue('authenticity_token','###123###')
query = form.getvalue('q','###123###')
if query!= "###123###" and token!="###123###" and csrf.decrypt(token):
	CR.getQuery(query.strip().lower())

else:
	res["error"]="Unauthorized Access"
	print json.dumps(res)
