from pymongo import MongoClient as MC
client = MC()
import re

disc = ["when","is","festival","fest","festivals","dates","in","month","day","th","st","nd","on","fall","falls","are","date","day","falling","holiday","holidays"]

days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]

months =["january","jan","february","feb","march","april","may","june","july","august","september","sept","october","oct","november","nov","dec","december"]

getMonths = {"january":"january","jan":"january","feb":"february","february":"february","march":"march","april":"april","may":"may","june":"june","jun":"june","july":"july","jul":"july","august":"august","aug":"august","september":"september","sept":"september","oct":"october","october":"october","november":"november","nov":"november","dec":"december","december":"december"}

getDays = {"mon":"monday","monday":"monday","tuesday":"tuesday","tue":"tuesday","wed":"wednesday","wednesday":"wednesday","thursday":"thursday","thu":"thursday","friday":"friday","fri":"friday","sat":"saturday","saturday":"saturday","sun":"sunday","sunday":"sunday"}

def main(query):

    query = query.lower()

    year = re.findall('[0-9]{4}',query)
    query = re.sub('[0-9]{4}',' ',query)
    date = re.findall('\d+',query)
    query = re.sub('\d+'," ",query)
    query = query.split()
    query=removeDisc(query)
    month = getMonth(query)
    day = getDay(query)
    frame = {}
    if date:
        frame["date"]=date
    if day:
        frame["day"]=day.capitalize()
    if month:
        
        frame["month"]=month
    if date:
        frame["date"]=date[0]
    if year:
        frame["year"]=year[0]
    if query:
        frame["name"]={"$regex":".*"+".*".join(query)+".*","$options":"i"}
    

    

    return get_answer(frame)
#    print (query)
#    print (year)
#    print (date)
#    print (day)
#    print (month)

    
    


def removeDisc(query):
    subQuery =[]
    for q in query :
        #print (q)
        if q not in disc :
            
            subQuery.append(q)
    return subQuery
def getMonth(query):

    for q in query :

        if q in months:
            query.remove(q)
            return getMonths[q]
    return ""


def getDay(query):

    for q in query :

        if q in days:
            query.remove(q)
            return getDays[q]
    return ""



############################# mongo operations ######################################
from pymongo import MongoClient as MC
client = MC()
db = client.kbmain
def get_answer(frame):
    #print (frame)
    if frame:
        ans= db.festivals.find(frame,{'_id':0})#.sort({"date":1})
        return [{"festivals":list(ans)}]
    else :
        return [{}]
