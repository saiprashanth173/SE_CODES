#!/usr/bin/python
import cgi,cgitb,json
import decryptCSRF as csrf
form = cgi.FieldStorage() 
print "Content-type:text/javascript\r\n\r"
res={}
token=form.getvalue('authenticity_token','###123###')
f = form.getvalue("q","##123##") #Gets input from the form
import test2
if f!="##123##" and token!="###123##" and csrf.decrypt(token):
    try:
       result = test2.get(f) #Gets result out of the smart answer module
      
       if len(result)!=0:
          result=result[0]
          key=result.keys()[0]
          
          if type(result[key]) is list:
             lisItems =result[key]
	     for item in lisItems:
                 if item.has_key('_id'):
                    item.pop('_id')
                 indx=lisItems.index(item)
                 lisItems[indx]=item
             result[key]=lisItems
             print json.dumps(result)
          else:
             if result[key].has_key('_id'):
 	        result[key].pop('_id')
             print json.dumps(result)
       else:
          print "{}"
    except Exception as x:
    	a={}
    	a["wiki"]=[]
    	print json.dumps(a)
else:
   res["error"]="Unauthorized Access"
   print json.dumps(res)
