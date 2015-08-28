# queries

# cricketer <name>
# which cricketer scored max|min|mostno of runs|

import re
ans = [{"cricket-players":{"required":[]}}]

disc = ["with","stats","statistics","player","a","cricketer","cricket","how","many","team","who","is","the","in","which","number","no","number","of","player","taken","match","matches","details","players","about","took","did","cric","by"]
bowling = ["wickets","wicket","bowling","economy","bowler"]
batting = ["high score","scored","highest score","highestscore","highscore","score","runs","strike rate","strikerate","batting","batter","batsmen","hundreds","hundred","tons","half centuries","half century","halfcenturies","halfcentury"]
teams = ["indian","india","ind","srilankan","srilanka","sl","sri lankan","sri lanka","south african","south africa","southafrican","southafrica","sa","new zealand","nz","newzealand","pakistan","pk","zimbabwe","bangladesh","bang","australian","australia","aus","kenyan","kenya"]
getTeams = {"india":"india","indian":"india","ind":"india","srilanka":"sri lanka","srilankan":"sri lanka","sl":"sri lanka","south african":"south africa","south african":"south africa","southafrica":"south africa","sa":"south africa","southafrican":"south africa","new zealand":"new zealand","newzealand":"new zealand","nz":"new zealand","pakistan":"pakistan","pk":"pakistan","zimbabwe":"zimbabwe","aus":"australia","australia":"australia","australian":"australia","kenyan":"kenya","kenya":"kenya"}

matchIdentifier = ["test","odis","odi","first class","tests"]
team = ""
query=""
matchType = "odi"
getMatch = {"odi":"ODIs","odis":"ODIs","test":"Tests","first class":"First-class","tests":"Tests"}
subValues = {"score":"Runs","runs":"Runs","strike rate":"SR","strikerate":"SR","high score":"HS","highscore":"HS","highestscore":"HS","highest score":"HS","hundreds":"100","hundred":"100s","centuries":"100s","tons":"100s","halfcenturies":"50","halfcentury":"50","economy":"Econ","wicket":"Wkts","wickets":"Wkts"}


def getQuery(query_input):
    global query,team
    
    query = query_input.lower()
    
    removeDiscarders()
    
    for tem in teams:
        if tem in query:
            team = getTeams[tem]
            query=query.replace(tem,"")
            break
       

    for bowl in bowling:
        if bowl in query:
            return getBowling()
            break

    for bat in batting:
        if bat in query:
            return getBatting()
            break
        
    return getDirect()
    

def removeDisc(lists):
    global query
    for lis in lists:
        if lis in query:
            query=query.replace(lis,"")
    
def getDirect():
    
    global ans,query
    #print query
    getMatchIdentifier()
    ans[0]["cricket-players"]["required"].append('player-info')
    ans[0]["cricket-players"]["required"].append(matchType)
    ters =  getvalues()
    if ters:
        ans[0]["cricket-players"]["main-ans"]=ters
    
    return ans
    
def removeDiscarders():
    queryList = []
    global query
    for querySplit in query.split():
        if querySplit not in disc:
            queryList.append(querySplit)

    query = " ".join(queryList)


def getBatting():
    global query,ans
    ans[0]["cricket-players"]["required"].append('BATTING')
    types =getMinMax()
    getMatchIdentifier()
    ans[0]["cricket-players"]["required"].append(matchType)
    if types=="min":

        getMain = getWord(batting)
        ters = getAggregated("min","BATTING",getMain)

        if ters:
            ans[0]["cricket-players"]["main-ans"]=ters
        return ans
        
    elif types == "max":
        getMain = getWord(batting)
        ters = getAggregated("max","BATTING",getMain)

        if ters:
            ans[0]["cricket-players"]["main-ans"]=ters
        return ans
    else:
        getMain = getWord(batting)
        ters = getAggregated("max","BATTING",getMain)
        if ters:
            ans[0]["cricket-players"]["main-ans"]=ters
        return ans
        
def getBowling():
    global query
    ans[0]["cricket-players"]["required"].append('BOWLING')
    types =getMinMax()
    getMatchIdentifier()
    ans[0]["cricket-players"]["required"].append(matchType)

    if types=="min":
        getMain = getWord(bowling)
        
        ters = getAggregated("min","BOWLING",getMain)

        if ters:
            ans[0]["cricket-players"]["main-ans"]=ters
        return ans

    elif types == "max":
        getMain = getWord(bowling)
        ters = getAggregated("max","BOWLING",getMain)

        if ters:
            ans[0]["cricket-players"]["main-ans"]=ters
        return ans


    
        
def getWord(lists):
    global query
    for lis in lists:
        #print lis
        if lis in query:
            
            query = query.replace(lis,"")
            if subValues.has_key(lis):
                removeDisc(lists)
                return subValues[lis]
                
    return ""
    
def getMatchIdentifier():
    global query,matchType
    matchSplit =[]
    for matchIdentity in matchIdentifier:
        if matchIdentity in query:
            matchType =matchIdentity
            query=query.replace(matchIdentity,"")
        
        
            
def getMinMax():
    global query
    types =""
    maximum = ["maximum","max","most","best"]

    minimum = ["minimum","min","lowest","least","worst"]

    for maxs in maximum:
        if maxs in query:
            query= query.replace(maxs,"")
            types = "max"

    if types :
        return types

    for mins in minimum:
        if mins in query:
            query= query.replace(mins,"")
            types = "min"

    return types
    
            
##################################### DB OPERATIONS #####################################################

from pymongo import MongoClient as MC
client = MC()
db = client.cricinfo


def getvalues():
    global ans,query
    content = db.players_main.find({"name":{"$regex":".*"+query.replace(" ",".*")+".*", "$options": "-i"}})
    
    k=list(content)
    if k: 
	k[0].pop("_id")
        return k[0]
    else:
        ans = [{}]
        return ""
    
def getAggregated(minmax,types,getMain):
    global ans,query
    import pymongo
    import re

    if not query.strip():
        if minmax=="min":
            if team:
                value=db.players_main.find({"team":re.compile(team, re.IGNORECASE)}).sort([(types+"."+getMatch[matchType]+"."+getMain,pymongo.ASCENDING)]).limit(1)
            else:
                value=db.players_main.find().sort([(types+"."+getMatch[matchType]+"."+getMain,pymongo.ASCENDING)]).limit(1)    
        elif minmax=="max":
            if team:
                value=db.players_main.find({"team":re.compile(team, re.IGNORECASE)}).sort([(types+"."+getMatch[matchType]+"."+getMain,pymongo.DESCENDING)]).limit(1)
            else:
                value=db.players_main.find().sort([(types+"."+getMatch[matchType]+"."+getMain,pymongo.DESCENDING)]).limit(1)

    else:
        value= db.players_main.find({"name":{"$regex":".*"+query.replace(" ",".*")+".*", "$options": "-i"}})

    value= list(value)

    if value:
	value[0].pop("_id")
        return value[0]
    else:
        ans=[{}]
        return ""

