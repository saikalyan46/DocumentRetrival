from collections import Counter
import re
from nltk.tokenize import RegexpTokenizer
import csv

tokenizer = RegexpTokenizer(r'\w+')
f = open("corpus1", encoding="utf8")
file_content = f.read()
f.close()
f = open("corpus1", encoding="utf8")

doc_id =[]
for line in f.readlines():  #storing the titles of documents alon with their title
    if '<doc' in line:
        tmp = line.split('\"')
        doc_id.append([int(tmp[1]),tmp[5]])
f.close()
raw= re.sub(r'<doc.*?>','&&&START&&&',file_content)
raw= re.sub(r'<.*?>','',raw)
raw = raw.split('&&&START&&&')
raw=list(filter(lambda x: x != "",raw))

main_dict={}
doc_counter=[]

for line in raw:    #tokenizing each document separately
    tokenize = tokenizer.tokenize(line)
    tokenize = [w.lower() for w in tokenize ]
    tokenize = Counter(tokenize)
    doc_counter.append(tokenize)

cnt=0
for doc_dict in doc_counter:    #creating the posting from the generated tokens
	for local in doc_dict.keys():
		if(local in main_dict.keys()):
			main_dict[local].append((doc_id[cnt][0],doc_dict[local]))
		else:
			main_dict[local]=[]
			main_dict[local].append((doc_id[cnt][0],doc_dict[local]))
	cnt+=1


with open('Inverted Index.csv', 'w', newline="", encoding = 'utf8') as csv_file:    #exporting the inverted index to csv file  
    writer = csv.writer(csv_file)
    for key, value in main_dict.items():
       writer.writerow([key, value])

with open('Document IDs.txt', 'w', encoding="utf8") as f:   #exporting the documents id and their corresponding title to a text file
    for item in doc_id:
        f.write(str(item[0])+" "+item[1]+'\n')