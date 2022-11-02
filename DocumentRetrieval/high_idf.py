import csv
import math
from collections import Counter

with open('Inverted Index.csv', 'r', encoding = 'utf8') as csv_file:
    reader = csv.reader(csv_file)
    index = dict(reader)

for ele in index:
    tmp = index[ele][1:len(index[ele])-1]
    tmp = tmp.replace('(','')
    tmp = tmp.replace(')','')
    tmp = tmp.replace(' ','')
    tmp = tmp.split(",")
    index[ele] = []
    for i in range(0, len(tmp), 2):
        index[ele].append([int(tmp[i]), int(tmp[i+1])])


doc_id=[]
map_doc_id_to_number_of_doc={}
map_word_to_number_of_word={}
doc_count=0
word_count=0

f=open('Document IDs.txt','r',encoding = 'utf8')
lines=f.readlines()

for line in lines:
	line=line.split(" ",1)
	doc_id.append([int(line[0]), line[1][:-1]])
	map_doc_id_to_number_of_doc[int(line[0])]=doc_count
	doc_count+=1



for word in index:
	map_word_to_number_of_word[word]=word_count
	word_count+=1

	
documents_as_vectors=[[0 for _ in range(int(doc_count))] for _ in range(word_count)]
        

def vectorizeDocuments():
    for word in index:
        for ele in index[word]:
            tf = ele[1]
            tf_wt = 1 + math.log10(tf)
            documents_as_vectors[map_word_to_number_of_word[word]][map_doc_id_to_number_of_doc[ele[0]]]=round(tf_wt, 3)



def cosine_generation():
    for i in range(doc_count):
        sum = 0
        for j in range(word_count):
            sum += documents_as_vectors[j][i] ** 2
        cos = 1/math.sqrt(sum)
        for j in range(word_count):
            documents_as_vectors[j][i] = round(documents_as_vectors[j][i] * cos, 3)

def evaluateQuery(str):     #generate top k by using high idf to eliminate the query terms which are deemed unecessary 
    
    array=str.split(' ')
    ci=Counter(array)
    tmp = [0 for _ in range(word_count)]
    mx=0
    tmp_query = []

    for key,value in ci.items():
        if key not in map_word_to_number_of_word.keys():
            continue
        df=len(index[key])
        idf=math.log10(doc_count/df)
        mx=max(mx,idf)
    mx/=2
    cn = []

    for key,value in ci.items():
        if key not in map_word_to_number_of_word.keys():
            continue
        df=len(index[key])
        idf=math.log10(doc_count/df)
        if idf>=mx:
            cn.append(key)
    c=Counter(cn)

    for key,value in c.items():
        if key not in map_word_to_number_of_word.keys():
            continue
        tmp[map_word_to_number_of_word[key]]=1+math.log10(value)
        df=len(index[key])
        idf=math.log10(doc_count/df)
        tmp[map_word_to_number_of_word[key]]*=idf
    sum = 0
    for j in range(word_count):
        sum += tmp[j] ** 2
    cos = 1/math.sqrt(sum)
    for j in range(word_count):
        tmp[j]*=cos
    score = []
    for i in range(doc_count):
        sum=0
        for j in range(word_count):
            sum+=tmp[j]*documents_as_vectors[j][i]
        score.append([sum, doc_id[i][1]])
    score.sort(key = lambda x:x[0], reverse = True)
    return score[:10]



vectorizeDocuments()
cosine_generation()


Query = ["ministry of zambia", "Lowpel and Geowaltek Nigeria Limited founder", "Acalolepta Species"]
isRelevant = {"ministry of zambia":["Yes", "No", "No", "No", "No", "No", "No", "No", "No", "No"],
                "Lowpel and Geowaltek Nigeria Limited founder":["Yes", "No", "No", "No", "No", "No", "No", "No", "No", "No"],
                "Acalolepta Species":["Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes"]
                }


def print_query_result(query):      #printing out the top k docs
    top_k = evaluateQuery(query.lower())
    print("Query: "+query.ljust(150 - len("Query: "+query), ' '),end="")
    print("\n")
    tmp = isRelevant[query]
    for i in range(10):
        print(str(i+1)+".) "+"\tTitle: "+str(top_k[i][1]))
        print("\tScore: "+str(top_k[i][0]))
        print("\tIs Relevant?: "+ tmp[i])

for i in range(3):
    print_query_result(Query[i])


