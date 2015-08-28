def main(query):
	import re
	disc = ["status","confirmation","confirm","statuses","yesterday","today","tomorrow","current","previous","late","fast",
                "arrival","train","trains","from","to","and","between"]
	x = query.split()
    	for i in range(0,len(disc)):
		if disc[i] in x:
			x.remove(disc[i])
    	query = " ".join(x)
    	match = re.match(r'\d+',query)
    	if match:
		query = query.strip()
        	query = int(query)
    	if(isinstance(query,(int))):
        	fin_result = query_num(query)
    	else:
        	fin_result = query_name(query)
		#fin_result = filter_result(result,query)
    	return fin_result

def filter_result(result,query):
	fin_result = []
	query = query.split()
	for i in range(0,len(result)):
		temp = result[i]
		temp2 = temp['Train Name'].lower().split()
		for j in range(0,len(query)-1):
			if temp2.index(query[j])>temp2.index(query[j+1]):
				continue
			else:
				fin_result.append(temp)
	return fin_result



def query_num(num):
	result = ""
	import MySQLdb,connection
	db= connection.connect("rig")
	cur = db.cursor(MySQLdb.cursors.DictCursor)
	sql="SELECT `trainname` AS `Train Name`,`text` As `Description`,`sstatus` AS `Status`,`lstatus` AS `Status Description` FROM `train` WHERE `trainnum`="+"%d"%num
	#print sql
    	cur.execute(sql)
   	result=cur.fetchall()
    	return result



def query_name(name):
	result = ""

        import MySQLdb,connection
        db= connection.connect("rig")

	cur = db.cursor(MySQLdb.cursors.DictCursor)
	name=name.split()
	sql="SELECT `trainname` AS `Train Name`,`text` As `Description`,`sstatus` AS `Status`,`lstatus` AS `Status Description` FROM `train` WHERE (`text` LIKE '"

	for i in range(0,len(name)):
		if(i<len(name)-1):
	        	sql = sql+"%"+name[i]
		else:
			sql = sql+"%"+name[i]+"%');"
        
        #print sql
	cur.execute(sql)
	
    	result=cur.fetchall()
	return result
