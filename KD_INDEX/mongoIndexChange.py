from pymongo import MongoClient as mc
import re
import getword
client=mc()

db = client.kb #this is to select the database

#field names to be ignored
nolist=['id','sno','SNo','Sno','_id','address','city','Address','Contact','contact','courses','description','Ministry','Group','Websites','district','District','misc','state','State','definition','addr','ph','type','email','phone_number','end','start','Length','Functioning','States','length_state','length_total','Head_quarters']

#collections to be ignored
notable=['retriv','rlink','movies_reviews','train','neft','bse','weather','wordgraph','food','pubs','religious','restaurant','shops','tagline','todo','tsunami','newIndex1','newIndex','newIndex2','hotels','hospitals','places','bankdetails','opinion_poll','religiuos','exams','system.indexes']


dicti={}
def runFun():
    collections=db.collection_names()
    collections.pop(0)
    
    for collection in collections:
        if collection not in notable:
            print collection

            data=db[collection].find()

            getDataFromCollections(str(collection),data)
        


def getDataFromCollections(collection,data):

    k=[]
    global dicti
    for dat in data :
        
      #  print dat
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
    #    print newDict
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

        varKeys=getword.getwordtonum([word])

        if varKeys:
            k=varKeys.pop(0)
            for word in varKeys:
                if dicti.has_key(word):
                    subDict=dicti[word]
                    if subDict.has_key(collection):
                        superSubDict=dicti[word][collection]
                        if superSubDict.has_key(k):
                            subSuperSubDict=dicti[word][collection][k]
                            if subSuperSubDict.has_key(key):
                                dicti[word][collection][k][key]=int(subSuperSubDict[key])+1
                                    
                            else:
                                dicti[word][collection][k][key]=1
                                
                    else:
                        dicti[word][collection]={}
                        dicti[word][collection][k]={}
                        dicti[word][collection][k][key]=1
                else:
                    
                    dicti[word]={}
                    dicti[word][collection]={}
                    dicti[word][collection][k]={}
                    dicti[word][collection][k][key]=1

                            
            
            

        
runFun()
import addFieldsIndex
db.newIndex2.update({'keyword':'india'},{"$set":{"mps": "categories","nationalparks": "categories","cabinet":"categories","judges":"categories"}},True)
db.newIndex2.update({'keyword':'sea'},{"$set":{"waterbodies": "categories"}},True)
db.newIndex2.update({'keyword':'lake'},{"$set":{"waterbodies": "categories"}},True)
db.newIndex2.update({'keyword':'river'},{"$set":{"waterbodies": "categories"}},True)
                    

