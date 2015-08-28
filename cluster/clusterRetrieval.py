import mainGla
from pymongo import MongoClient as MC
from collections import Counter as Count
client = MC("192.168.103.25")
db = client.testIndex
import time,json

# retrieves list of ids
def getFromMongo(query):
    lis = []
    lists = db.test.find({"keyword":{"$in":query}},{"keyword":0,"_id":0})

    final = Count({})
    for lis in lists:
        
        final+= Count(lis)
        
    lis=sorted(final, key=final.get, reverse=True)    
    lis = tuple(lis[:3000])
    return lis
    
    
def getClusteredResults(lis):
    lis= lis.replace("u'","'")

    import MySQLdb
    mysqldb = MySQLdb.connect('127.0.0.1','root','#srmseONserver1','test')
    cursor = mysqldb.cursor()
    sql = "SELECT CONCAT(cluster,id) FROM `stor` WHERE id IN %s order by cluster,field(`id`,%s)"%(lis,lis[1:len(lis)-1])
    cursor.execute(sql)

    data = list(cursor.fetchall())
    return data

def getGrouped(lis):

    dicti = {}
    from itertools import groupby
    for k,v in groupby(lis,key=lambda x: str(int(x[0]))[:3]):
        dicti[k]= map(removeWaste,v)

    return dicti
def removeWaste(tup):
    return str(tup[0])[3:]

    
def getQuery(query):
    import mainGla as MG
    start = time.time()
    
    query = MG.removeUnwanted(query.split())
    content = getFromMongo(query)
    if content:
        data = getClusteredResults(str(content))
        mainResult = getGrouped(data)
    
        print  json.dumps(mainResult)
    else:
        print {}    

