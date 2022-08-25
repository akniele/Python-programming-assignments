# Simple information retrieval system for presidential inaugural speeches

## Program description
This program allows users to search for words and two-word phrases in the Inaugural Address Corpus provided by the NLTK library.
Users can choose to enter one or two words/phrases. The program outputs a list of all the documents within the corpus that contain these words/phrases.
When searching for two words/phrases users can choose between only retrieving documents that contain both words/phrases (*AND*),
and retrieving all documents that contain at least one of the two, or both (*OR*). Additionally, the user can specify to negate (*NOT*) one or both of the two terms/phrases. Boolean operators are used for this.

## Structure of the program
The program contains nine functions:
* tokenize_documents
* bigrams_documents
* def_value
* token_dictionary
* bigram_dictionary
* negation*
* intersect
* union
* main

*tokenize_documents* and *bigrams_documents* are used to created a list of tuples containing all the words/bigrams, respectively, and the document id of the document the word/bigram occured in.
They return a list that is sorted alphabetically by the first letter of the string, and then further sorted by document id (the oldest speeches come first).
*def_value* is a helper function used to initialize the default value in the default dictionaries used in functions *token_dictionary* and *bigram_dictionary*.
These two functions return a dictionary containing the words/bigrams as keys, and a list of all the documents in which the words/bigrams occur as the corresponding value.
The functions *intersect* and *union* take two lists of document ids and return their intersection/union. The function *negation* returns the document IDs of all the documents
that don't contain the search term/phrase.
The *main* function deals with user input, finding out whether the user wants to search for words or bigrams, how many words/bigrams they want to search for, and whether they want to use the 
boolean AND or OR. It then prints the document ids that match the user's query and asks if the user would like to make another search. 

## How to run the program
*main* is called automatically when the python file is run. It will continue to call itself until the user answers 'no' ('n') when asked whether they would like to do another search.
There is also a test suite provided, *test_suite.py*, containing code that can be used to find words/phrases that only occur in one document.
With these words, the user can test the programs functions. Here are some examples of words/phrases that only occur in one document:

* acquit
* actuate
* adore
* merited
* menaces
* 14th day
* a distrustful
* a recommendation
* civil administration
* collect my

If the user types in *adore AND merited* they get 'no documents found' as an output, seeing as both of these words only occur in one document, but not in the same document.
If the user types in *adore OR merited* they get '1789-Washington', '1797-Adams' as an output, seeing as 'adore' occurs in '1789-Washington' and 'merited' in '1797-Adams'.
If the user types *civil administration AND NOT collect my* they get 'no documents found' as an output, seeing as both of these phrases only occur in the
document '1789-Washington', but since we negated the phrase 'collect my' this document does not appear in the results.

