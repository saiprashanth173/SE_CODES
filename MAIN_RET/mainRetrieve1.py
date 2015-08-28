from pymongo import MongoClient as mc
from mergedict import MergeDict
import MySQLdb,json,re
import wiki
class SumDict(MergeDict):
    @MergeDict.dispatch(int)
    def merge_int(this, other):
        return this + other
class SumDict1(MergeDict):
    @MergeDict.dispatch(float)
    def merge_int(this, other):
        return this + other 
def getListQuery(lis,dbase,coll):
    from pymongo import MongoClient as mc
    from collections import Counter
    check = 0
    client = mc()
    if dbase == "testIndex":
        client = mc("192.168.103.25")
    if dbase=="wiki":
    	return wiki.main(lis)
    db = client[dbase]

    results=db[coll].find({"keyword":{"$in":lis}},{"keyword":0,"_id":0})
    listCounters = list(results)
    if dbase  == "news" or dbase == "youtube":
        if len(lis) == len(listCounters):
            return list(getNewContent(listCounters))
    else:
        check =1
    
    result=SumDict({})
    if check ==1:
    
        for listCounter in listCounters:
            result.merge(listCounter)
    
        sor=sorted(result, key=result.get, reverse=True)
        return sor
    else:
        return []


def getNewContent(contents):
    ids = []
    for content in contents:
        ids.append(set(content["ids"]))
    return set(ids[0]).intersection(*ids)


def remove(mongoDict):
    from collections import Counter

    mongoDict.pop('_id')
    mongoDict.pop('keyword')
    return mongoDict
    
