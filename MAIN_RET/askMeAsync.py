
#!/usr/bin/python

from threading import Thread as T
import threading,json
from Queue import Queue
import mainGla as MG
import mainRetrieve1 as MR
import che as SC
import fetchResults as FR


def getQuery(query,typ):
    k={"1":"general","2":"wiki","3":"news","4":"videos"}
    typ=k[typ]    
    dist={}

#    changed_query=SC.checking(query)
#    if query.lower() == changed_query.lower():
#	dist={"Did You Mean: ":""}
 #   else:
#	query=changed_query
#	dist = {"Did You Mean: ":query}
    query = query.lower()
    if typ == "videos":
        remove_videos = ["scene","scenes","videos","videos","clip","clips","videoclips","videoclip"]
        query = query.split()
        new_query = []
        for q in query:
            if q not in new_query:
                new_query.append(q)	
        query = " ".join(new_query)

    valuesDictionary = {"dictionary":["dictionary_db","dictionary_index","test","dictionary_table"],"news":["news","newNewsIndex","SRMSE","source21"],"wiki":["wiki","wiki3","my_wiki","page"],"general":["testIndex","test","test","source_main1"],"videos":["youtube","youtube_index","yt","main_links"]}
    if typ!="wiki":
    	query = MG.removeUnwanted(query.split(" "))
    else:
    	query=query.split()
    #print query
    get = valuesDictionary[typ]
    result = MR.getListQuery(query,get[0],get[1])
    #print get[0],get[1],result
    database = get[2]
    table = get[3]
    if (typ=="news"):
        result = sorted(result,reverse=True)
    if (typ=="general"):
	if len(result)>=10:
    	    topIds = result[:10]
        else:
            topIds = result
	topResults=[]
	if len(topIds)!=0:
                #print topIds
    		topResults = FR.fetchResults(topIds,database,table)
	dist["results"]=topResults
	dist["ids"]= result[10:100]
    elif (typ=="wiki"):
        topIds=result#by default you will get one result only
	topResults=[]
	if len(topIds)!=0:
        	topResults = FR.fetchResultsWiki(topIds,database,table," ".join(query))
        dist["results"]=topResults
        dist["ids"]= result[5:50]

    else:
	topIds=result[:5]
	topResults=[]
	if len(topIds)!=0:
		topResults = FR.fetchResults(topIds,database,table)
	dist["results"]=topResults
	dist["ids"]= result[5:50]            

    return dist
    
        
    

    
