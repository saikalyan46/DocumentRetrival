import numpy as np
import csv
import math
import time
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
champion_list = [[0 for _ in range(int(10))] for _ in range(word_count)]
        

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

def championsList(): #genrate champion list of every word present in the dictionary
    for i in range(word_count):
        tmp = []
        for j in range(doc_count):
            tmp.append([documents_as_vectors[i][j], doc_id[j][0]])
        tmp.sort(key = lambda x:x[0], reverse = True)
        for k in range(10):
            champion_list[i][k] = tmp[k][1]

def evaluateQuery(str):     #generate top k using the chapion lists 
    array=str.split(' ')
    c=Counter(array)
    tmp = [0 for _ in range(word_count)]
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
    champion_documents=[]
    for word in array:
        for docid in champion_list[map_word_to_number_of_word[word]]:
            champion_documents.append(docid)
    champion_documents = np.unique(np.array(champion_documents)) 
    for i in range(len(champion_documents)):
        sum=0
        for j in range(word_count):
            sum+=tmp[j]*documents_as_vectors[j][map_doc_id_to_number_of_doc[champion_documents[i]]]
        score.append([sum, champion_documents[i]])
    score.sort(key = lambda x:x[0], reverse = True)
    return score[:10]



vectorizeDocuments()
cosine_generation()
championsList()


Query = ["ministry of zambia", "Lowpel and Geowaltek Nigeria Limited founder", "Acalolepta Species"]
isRelevant = {"ministry of zambia":["Yes", "No", "No", "No", "No", "No", "No", "No", "No", "No"],
                "Lowpel and Geowaltek Nigeria Limited founder":["Yes", "No", "No", "No", "No", "No", "No", "No", "No", "No"],
                "Acalolepta Species":["Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes","Yes"]}

total = 0
def print_query_result(query):      #printing out the top k docs
    global total
    start = time.time()
    top_k = evaluateQuery(query.lower())
    total += time.time() - start
    print("Query: "+query.ljust(150 - len("Query: "+query), ' '),end="")
    print("\n")
    tmp = isRelevant[query]
    for i in range(10):
        print(str(i+1)+".) "+"\tTitle: "+[x[1] for x in doc_id if x[0] == top_k[i][1]][0])
        print("\tScore: "+str(top_k[i][0]))
        print("\tIs Relevant?: "+ tmp[i])

for i in range(len(Query)):
    print_query_result(Query[i])

# original average time for each query = 3.7951985200246177secs
# championlist, query processingspeed = 0.31018487612406415secs
print("\nOn an average each query processing takes about "+str(3.7951985200246177)+" seconds in the original one.")
print("While in Championlist indexing, the query processing is done on an average of "+str(total/3)+ " seconds.")
print("About " +str(((3.7951985200246177-(total/3)/3.7951985200246177)*100))+"% improvement in query processing speed")


