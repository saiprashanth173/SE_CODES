from pymongo import MongoClient as mc
import re
client=mc()

db = client.kb #this is to select the database

nolist=['id','sno','SNo','Sno','_id']
notable=['retriv','rlink','movies_reviews','train','neft','bse','weather','wordgraph','food','pubs','religious','restaurant','shops','tagline','todo','tsunami','newIndex1','newIndex','newIndex2','hotels','hospitals','places','bankdetails','opinion_poll','religiuos','exams','system.indexes']

dicti={}
def runFun():
    collections=db.collection_names()
    collections.pop(0)
    for collection in collections:
        if collection not in notable:
            collection=str(collection)

            data=db[collection].find()
            storeField(collection,data)


def storeField(collection,data):

    fields=data[0].keys()

    for field in fields:
        field=str(field).lower()
        if field not in nolist:
            if dicti.has_key(field):
                dicti[field][collection]="field"
            else:
                dicti[field]={}
                dicti[field][collection]="field"
    addToDbase()


def getDataFromCollections(collection,data):

    k=[]
    global dicti
    for dat in data :
        
        k=dat.keys()
        for key in dat.keys():
            key=str(key)
            if key not in nolist and dat[key]:
                regex=re.compile('[%s]'% re.escape('!"#$%&\'()*+,-.:;<=>?@[\\]^_`{|}~'))
                content=str(dat[key]).lower()
                content=re.sub(regex," ",content)
                addToDict(collection,content,key)
    addToDbase()


def addToDbase():
    global dicti
    for key in dicti.keys():
        checkDict={}
        checkDict["keyword"]=key
        newDict=dicti[key]
        newDict.update({"keyword":key})
        db.newIndex2.update(checkDict,{"$set":newDict},True)
    
    dicti={}

def addToDict(collection,content,key):

    global dicti
    words=content.split()

    for word in words :
        word=str(word)
        if dicti.has_key(word):
            subDict=dicti[word]
            if subDict.has_key(collection):
                superSubDict=dicti[word][collection]
                if superSubDict.has_key(key):
                    dicti[word][collection][key]=int(superSubDict[key])+1
            
                else:
                    dicti[word][collection][key]=1
            else:
                dicti[word][collection]={}
                dicti[word][collection][key]=1
        else:
            dicti[word]={}
            dicti[word][collection]={}
            dicti[word][collection][key]=1
        
runFun()

