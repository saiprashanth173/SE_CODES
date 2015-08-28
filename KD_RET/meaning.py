from pymongo import MongoClient as MC
client = MC()
db = client.Dictionary
stopWords = ['does','what','mean']
acceptWords = ['mean','meaning','means','meant']
def removeWordsDict(query):
    import re
    words = re.findall('what is the meaning of (.+)|what does the word (.+) mean|meaning of (.+)|(.+) means|what meaining of (.+)|meaning of (.+)|meaning (.+)|what (.+) means|what is (.+)|define (.+)|definition of (.+)|(.+) definition|(.+) meaning|(.+) means|(.+) means what|whats meaning of (.+)|what does (.+) mean',query) 
    word = []
    if words:
       word = filter(lambda x:x!='', list(words[0]))
    elif len(query.split(" "))==1:
	word = [query]
    return ''.join(word)
    

def newWordEntry(keyword):
    import MySQLdb
    try:
        con = MySQLdb.connect(host="127.0.0.1",user="root",passwd="#srmseONserver1",db="rig")
    	cursor = con.cursor()
    	cursor.execute("INSERT INTO newWord(keyword,count) VALUES (%s,%s)",(keyword,"0"))
    	con.commit()
    	con.close()
    except:
        pass


def getKeyword(query):
    query = query.strip()
    query = removeWordsDict(str(query))
    return str(query)

def properDict(cursor):
    output= {'dict':{}}
    for item in cursor:
        item.pop('_id')
        output['dict'] = item
        break
    return output
def main(query):
    keyword = getKeyword(str(query))
    keyword = str(keyword).strip()
    cursor = db.dictionary.find({'keyword':str(keyword)})
    dicto = properDict(cursor)
    if dicto['dict']:
    	return dicto
    else:
	newWordEntry(keyword)
	return dicto
