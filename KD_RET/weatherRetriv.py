import json
import MySQLdb,connection
db= connection.connect("rig")

cursor=db.cursor(MySQLdb.cursors.DictCursor)
import re,time
import string
import datetime

def removePandS(content):
    re.sub(r'\b\w{,2}\b',' ', content)
    re.sub(r'\b\w{15,}\b',' ', content)
    regex=re.compile('[%s]'% re.escape(string.punctuation))
    content=re.sub(regex," ",content)
    stop_words=set(["weather","a","a's","belongs","able","about","above","according","accordingly","across","actually","after","afterwards","again","against","ain't","all","allow","allows","almost","alone","along","already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","aside","ask","asking","associated","at","available","away","awfully","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","c'mon","c's","came","can","can't","cannot","cant","cause","causes","certain","certainly","changes","clearly","co","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't","course","currently","definitely","described","despite","did","didn't","different","do","does","doesn't","doing","don't","done","down","downwards","during","each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","far","few","fifth","first","five","followed","following","follows","for","former","formerly","forth","four","from","further","furthermore","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","had","hadn't","happens","hardly","has","hasn't","have","haven't","having","he","he's","hello","help","hence","her","here","here's","hereafter","hereby","herein","hereupon","hers","herself","hi","him","himself","his","hither","hopefully","how","howbeit","however","i'd","i'll","i'm","i've","ie","if","ignored","immediate","in","inasmuch","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isn't","it","it'd","it'll","it's","its","itself","just","keep","keeps","kept","know","known","knows","last","lately","later","latter","latterly","least","less","lest","let","let's","like","liked","likely","little","look","looking","looks","ltd","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover","most","mostly","much","must","my","myself","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","particular","particularly","per","perhaps","placed","please","plus","possible","presumably","probably","provides","que","quite","qv","rather","rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","shouldn't","since","six","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","t's","take","taken","tell","tends","th","than","thank","thanks","thanx","that","that's","thats","the","their","theirs","them","themselves","then","thence","there","there's","thereafter","thereby","therefore","therein","theres","thereupon","these","they","they'd","they'll","they're","they've","think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together","too","took","toward","towards","tried","tries","truly","try","trying","twice","two","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","value","various","very","via","viz","vs","want","wants","was","wasn't","way","we","we'd","we'll","we're","we've","welcome","well","went","were","weren't","what","what's","whatever","when","whence","whenever","where","where's","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","who's","whoever","whole","whom","whose","why","will","willing","wish","with","within","without","won't","would","wouldn't","yes","yet","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"])
    a=" ".join(word for word in content.split() if word not in stop_words)
    return a.split()


def hourly(city,time):
    if len(str(time))==1:
        time="0"+str(time)
    
    sql = "SELECT * FROM weatherhourly WHERE city='%s' and time='%s'"%(city,time)
  
    cursor.execute(sql)
    data=cursor.fetchone()
    return data

def general(city):
    city="%"+city+"%"
    sql = "SELECT * FROM weather WHERE city like \'"+city+"\'"
    cursor.execute(sql)
    data=cursor.fetchone()

    sql = "SELECT * FROM weatherforecast WHERE city like \'"+city+"\'"
    cursor.execute(sql)

    cont=cursor.fetchall()
    data["day"] = time.strftime("%A")[:3]
    data["future"]= list(cont)
    return data

def forecast(city,days):
    city="%"+city+"%"
    sql = "SELECT * FROM weatherforecast WHERE city like \'"+city+"\' and time='%s'"%(days)
#    print sql
    cursor.execute(sql)
    data=cursor.fetchone()
    return data


def queryRetriv(query):

    query=removePandS(query)
    hours=['hour','hours','hrs']
    days=['days','day','tomorrow']
    day=datetime.datetime.now().day
    hour=datetime.datetime.now().hour
    interHour=list(set(hours) & set(query))
    interDay=list(set(days) & set(query))
    
    if interHour:
        for interH in interHour:
            query.pop(query.index(interH))
        num=map(str,range(1,25))
        numintersection=list(set(num)&set(query))
        if numintersection:
            
            innum=numintersection[0]
            query.pop(query.index(innum))
            hour+=int(innum)
            if (hour>=24):
                hour=hour-24
            
        else :
            hour+=1
        city=query[0]
        data=hourly(city,hour)
    elif interDay:
        for interH in interHour:
            query.pop(query.index(interH))
        num=map(str,range(1,25))
        day=0
        numintersection=list(set(num)&set(query))
    
        if numintersection:           
            if len(numintersection)==1:
                innum=numintersection[0]
                query.pop(query.index(innum))
                day+=int(innum)
        elif len(interDay)==2:
            day+=2
        else :
            day+=1

        city=query[0]
        data=forecast(city,day)
        
    else:
        city=query[0]
        

        data=general(city)

    return data
        

        
