# Ranked retrieval system for United Nations document

## Program description
This program allows users to pass in a search query consisting of multiple words. It then returns the document IDs of the top five UN documents that best match the search query.

For instance, the user could input the query *health insurance*, one word at a time. When using cosine similarity as the similarity metric (users get to choose between this and a non-normalized metric), the following documents are retrieved by the system:

*docs46.txt*, *docs15.txt*, *docs32.txt*, *docs48.txt*, *docs27.txt*

These are the five documents that best match the user's query. 


## How to run the program
First, the file *divide_file.py* should be used to divide *doc1* (the first United Nations file) into fifty smaller files before running *retrieval.py*. When the file *retrieval.py* is then run,*main* is called automatically and will continue to call itself until the user answers 'no' ('n') when asked whether they would like to do another search. 



