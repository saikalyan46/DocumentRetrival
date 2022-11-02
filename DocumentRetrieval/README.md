# Document-Retrieval
First run the Preprocessing.py file to generate the intermediate files.</br>
Then run the main.py file for checking out the output of the queries of the initial implementation of IR system.</br>
The remaining files are the ones where the implementation of improvements are done.</br>
Run them individually.

## Required libraries
nltk</br>
re</br>
autocorrect</br>

## IMPLEMENTATION
1) Library used nltk, re, csv.</br>
2) Text cleaning and punctuation removal is done with re and the tokenization
is done with nltk.
3) In main.py an inverted index is built from the corpus in the form of a
dictionary. And the doc id along with its respective title is stored in another
array.</br>
4) The processed corpus is converted to Inverted index and stored in a csv file
which is then exported using csv library.</br>
5) The doc ids and titles are exported to a text file.</br>
6) The csv file is then imported and used for building the vector space model
where then the inputted query is processed from the built vector space
model, giving out results.</br>
7) The same processing file which constructs the vector space model is again
used to implement the issues correction we have noticed within the code
of the implementation.</br>

## IMPROVEMENTS TO main.py
ISSUE 1</br>
1) HIGH LATENCY - Score computation is a large (10s of %) fraction of the, CPU
work on a query, Generally, we have a tight budget on latency We’ll look at
ways of cutting CPU usage for scoring, without compromising the quality of
results (much).</br>
2) CHAMPION LIST-For every term (t), store a list of r documents that have the
highest score for term t, The score we are using weight score.r is fixed atthe index creation time, thus it’s possible that r< K. The set of r documents
are called the champion list for term t. Now, for a query, create a set of
documents A from the champion list of all the terms in the query.</br>
3) Decrease in the number of documents will result in low latency.</br>
4) This is an inexact way of finding top r documents, corner cases might exist.
example- weights are almost equal in more than r elements.</br>
5) With the same queries in the original and modified ones, we have
calculated their processing speed and checked out its improvement ratio
from its predecessor.</br>
![image](https://user-images.githubusercontent.com/54111714/140653974-b2ddd496-1bba-4f40-8dcd-29f67a1c8fcf.png)
It had a 371.3 % improvement in processing speed.</br>

## ISSUE 2
1) High frequency of some words such as stop words will increase the score of
some documents ,since stop words are not the prime indicators of
relevance of a document, the weight of stop words should be lesser than
rare words.</br>
2) In query, calculate IDF of every term, store the maximum IDF value, ignore
the terms with IDF value lesser than half of the maximum value of IDF.</br>
3) Less frequent words are given more importance than more frequent words,
it will increase the probability of extracting more relevant documents.</br>
4) Ignoring some words might cause some inconsistency in search.</br>
![image](https://user-images.githubusercontent.com/54111714/140654015-b792a958-87a8-422a-8fdf-56835a172567.png)
![image](https://user-images.githubusercontent.com/54111714/140654021-6467061b-3afe-42d0-80f3-7ae358471e68.png)
![image](https://user-images.githubusercontent.com/54111714/140654024-9fc694fa-be43-4765-b4c3-08a61a1472e4.png)

## ISSUE 3
1) The IR system in main.py has no way to check whether the entered term of
the query is correct in spelling. This results in unexpected consequences in
the final output.</br>
2) A spell corrector can be implemented using many dependable open source
libraries. Each term of the query undergoes correction if the term is not
available in the dictionary.</br>
3) The imported libraries correct the spelling of the term and undergoes the
query processing to correct results.</br>
4) It does not always yield the expected correct term of its respective
incorrectly entered term. This might cause the IR system to give an overall
different result to the query.</br>


| Before correction | After correction |
| --- | --- |
| <img src="https://user-images.githubusercontent.com/54111714/140654067-7026870d-90c2-4e96-92cc-bad14e85f37a.png" align="left"> | <img src="https://user-images.githubusercontent.com/54111714/140654103-88a08c56-542a-482f-a7da-6c254570dc0b.png" align="right"> |
| <img src="https://user-images.githubusercontent.com/54111714/140654105-096e533c-3b38-44b6-8276-e4c0a1094768.png" align="left"> | <img src="https://user-images.githubusercontent.com/54111714/140654084-2bf615e1-2cd8-4700-ac10-82038d5871a7.png" align="right"> |
| <img src="https://user-images.githubusercontent.com/54111714/140680250-5064f00e-c67a-4425-9ea5-aa7d887a9b40.png" align="left"> | <img src="https://user-images.githubusercontent.com/54111714/140654110-4f7fd8a4-ed5f-4a13-801f-509a5ea7fbde.png" align="right"> |
