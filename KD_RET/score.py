import MySQLdb
import urllib2
import re
import string 
db=MySQLdb.connect('127.0.0.1','root','#srmseONserver1','rig')
cursor=db.cursor()

def removePandS(content):

    re.sub(r'\b\w{,2}\b',' ', content)
    re.sub(r'\b\w{15,}\b',' ', content)
    regex=re.compile('[%s]'% re.escape(string.punctuation))
    content=re.sub(regex," ",content)
    stop_words=set(["cricket","scoreboard","live","scorecard","match","latest","score","batting","bowling","wicket","wickets","runs","bowler","batter","batsman","a","a's","belongs","able","about","above","according","accordingly","across","actually","after","afterwards","again","against","ain't","all","allow","allows","almost","alone","along","already","also","although","always","am","among","amongst","an","and","another","any","anybody","anyhow","anyone","anything","anyway","anyways","anywhere","apart","appear","appreciate","appropriate","are","aren't","around","as","aside","ask","asking","associated","at","available","away","awfully","be","became","because","become","becomes","becoming","been","before","beforehand","behind","being","believe","below","beside","besides","best","better","between","beyond","both","brief","but","by","c'mon","c's","came","can","can't","cannot","cant","cause","causes","certain","certainly","changes","clearly","co","com","come","comes","concerning","consequently","consider","considering","contain","containing","contains","corresponding","could","couldn't","course","currently","definitely","described","despite","did","didn't","different","do","does","doesn't","doing","don't","done","down","downwards","during","each","edu","eg","eight","either","else","elsewhere","enough","entirely","especially","et","etc","even","ever","every","everybody","everyone","everything","everywhere","ex","exactly","example","except","far","few","fifth","first","five","followed","following","follows","for","former","formerly","forth","four","from","further","furthermore","get","gets","getting","given","gives","go","goes","going","gone","got","gotten","greetings","had","hadn't","happens","hardly","has","hasn't","have","haven't","having","he","he's","hello","help","hence","her","here","here's","hereafter","hereby","herein","hereupon","hers","herself","hi","him","himself","his","hither","hopefully","how","howbeit","however","i'd","i'll","i'm","i've","ie","if","ignored","immediate","in","inasmuch","indeed","indicate","indicated","indicates","inner","insofar","instead","into","inward","is","isn't","it","it'd","it'll","it's","its","itself","just","keep","keeps","kept","know","known","knows","last","lately","later","latter","latterly","least","less","lest","let","let's","like","liked","likely","little","look","looking","looks","ltd","mainly","many","may","maybe","me","mean","meanwhile","merely","might","more","moreover","most","mostly","much","must","my","myself","name","namely","nd","near","nearly","necessary","need","needs","neither","never","nevertheless","new","next","nine","no","nobody","non","none","noone","nor","normally","not","nothing","novel","now","nowhere","obviously","of","off","often","oh","ok","okay","old","on","once","one","ones","only","onto","or","other","others","otherwise","ought","our","ours","ourselves","out","outside","over","overall","own","particular","particularly","per","perhaps","placed","please","plus","possible","presumably","probably","provides","que","quite","qv","rather","rd","re","really","reasonably","regarding","regardless","regards","relatively","respectively","right","said","same","saw","say","saying","says","second","secondly","see","seeing","seem","seemed","seeming","seems","seen","self","selves","sensible","sent","serious","seriously","seven","several","shall","she","should","shouldn't","since","six","so","some","somebody","somehow","someone","something","sometime","sometimes","somewhat","somewhere","soon","sorry","specified","specify","specifying","still","sub","such","sup","sure","t's","take","taken","tell","tends","th","than","thank","thanks","thanx","that","that's","thats","the","their","theirs","them","themselves","then","thence","there","there's","thereafter","thereby","therefore","therein","theres","thereupon","these","they","they'd","they'll","they're","they've","think","third","this","thorough","thoroughly","those","though","three","through","throughout","thru","thus","to","together","too","took","toward","towards","tried","tries","truly","try","trying","twice","two","un","under","unfortunately","unless","unlikely","until","unto","up","upon","us","use","used","useful","uses","using","usually","value","various","very","via","viz","vs","want","wants","was","wasn't","way","we","we'd","we'll","we're","we've","welcome","well","went","were","weren't","what","what's","whatever","when","whence","whenever","where","where's","whereafter","whereas","whereby","wherein","whereupon","wherever","whether","which","while","whither","who","who's","whoever","whole","whom","whose","why","will","willing","wish","with","within","without","won't","would","wouldn't","yes","yet","you","you'd","you'll","you're","you've","your","yours","yourself","yourselves"])
    a=" ".join(word for word in content.split() if word not in stop_words)
    return a.split()


def scoreRetriv(query):
    querys=[]
   # print query
    if " vs " in query:
        querys = query.split(" vs " ,1)

    elif " v/s " in query:
        querys = query.split(" v/s " ,1)

    elif " versus " in query:
        querys = query.split(" versus " ,1)
    
    team1=" ".join(removePandS(querys[0]))
    team2=" ".join(removePandS(querys[1]))

    
    matchScore=score(team1,team2)
    return [matchScore]

        

def score(team1,team2):
    dicti={}
    cursor.execute("SELECT * FROM cricket WHERE teams LIKE '%"+team1+"%' and teams Like '%"+team2+"%' order by id desc")
    data=cursor.fetchall()
    content=list(data[0])
    content.pop(0)
    content.pop(0)
    general= content[1]
    content.pop(1)
    dicti['General']=general
    dicti['Score']=str(content[1])
    dicti['Overs']=str(content[0]).replace("ov","")
    if content[4] and content[3]!=content[4]:
        dicti['Batting']= content[3].replace("*","").strip()+" & "+content[4].replace("*","").strip()
    else:
        dicti['Batting']=content[3]
    dicti['Bowling']=content[5].strip()
    dicti['Status']=content[6].strip()
    dicti['Description']=content[7].strip()

    return dicti
