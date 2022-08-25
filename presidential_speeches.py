from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from collections import defaultdict
from nltk.corpus import inaugural


def tokenize_documents(document_list):
    tokenized_docs = []
    for doc in document_list:
        doc_id = doc.removesuffix(".txt")
        text = inaugural.raw(doc)
        words = word_tokenize(text)
        for word in words:
            if word.isalpha():
                tokenized_docs.append((word.lower(), doc_id))

    tokenized_docs_alpha = sorted(tokenized_docs)
    tokenized_docs_alpha_2 = sorted(tokenized_docs_alpha, key=lambda x: x[1])

    return tokenized_docs_alpha_2


def bigrams_documents(document_list, list_options):
    bigrams = []
    for doc in document_list:
        doc_id = doc.removesuffix(".txt")
        text = inaugural.raw(doc)
        sentences = sent_tokenize(text)
        for sentence in sentences:
            line_without_special_char = ''
            for character in sentence:
                if character not in list_options:
                    line_without_special_char += character

            token_words = word_tokenize(line_without_special_char)

            for i in range(len(token_words) - 1):
                bigram = token_words[i].lower() + " " + token_words[i + 1]
                bigrams.append((bigram, doc_id))

    bigrams_alpha = sorted(bigrams)
    bigrams_alpha_2 = sorted(bigrams_alpha, key=lambda x: x[1])

    return bigrams_alpha_2


def def_value():
    return "no documents found"


def token_dictionary(token_list):
    final_dict = defaultdict(def_value)
    for token in token_list:
        if token[0] not in final_dict:
            final_dict[token[0]] = [token[1]]
        elif token[0] in final_dict and token[1] not in final_dict[token[0]]:
            final_dict[token[0]].append(token[1])
    return final_dict


def bigram_dictionary(bigram_list):
    final_bigram_dict = defaultdict(def_value)

    for token in bigram_list:
        if token[0] not in final_bigram_dict:
            final_bigram_dict[token[0]] = [token[1]]
        elif token[0] in final_bigram_dict and token[1] not in final_bigram_dict[token[0]]:
            final_bigram_dict[token[0]].append(token[1])
    return final_bigram_dict


# based on pseudo-code from the lecture slides
def intersect(lst1, lst2):
    p1 = 0
    p2 = 0
    lst1 = list(lst1)
    lst2 = list(lst2)
    results = set()
    while p1 < len(lst1) and p2 < len(lst2):
        if lst1[p1] == lst2[p2]:
            results.add(lst1[p1])
            p1 += 1
            p2 += 1
        elif lst1[p1] > lst2[p2]:
            p2 += 1
        else:
            p1 += 1

    if not results:
        return "no documents found"
    return results


def union(lst1, lst2):
    results = set()
    for element in lst1:
        results.add(element)
    for element in lst2:
        if element not in lst1:
            results.add(element)
    return results


def negation(word, dictionary, document_list):
    documents = document_list.copy()
    try:
        contains_word = dictionary[word]
        for element in contains_word:
            documents.remove(element)
    except ValueError:
        pass
    documents = set(documents)
    return documents


doc_list = inaugural.fileids() # list of file names
options = "()*.,;:"

tokenized_doc_list = []
for doc in doc_list:
    doc_id = doc.removesuffix(".txt")
    tokenized_doc_list.append(doc_id)


list_of_tokens = tokenize_documents(doc_list)
dictionary_of_tokens = token_dictionary(list_of_tokens)  # create the term dictionary

list_of_bigrams = bigrams_documents(doc_list, options)
dictionary_of_bigrams = bigram_dictionary(list_of_bigrams)  # create the bigram dictionary


def main():
    word_or_phrase = input("Type '1' for a word query, '2' for a phrase query: ")
    while word_or_phrase != "1" and word_or_phrase != "2":
        word_or_phrase = input("Please type either '1' or '2: ")
    if word_or_phrase == "1":
        used_dictionary = dictionary_of_tokens
    else:
        used_dictionary = dictionary_of_bigrams
    first_word = input("Please state your query: ").lower()
    neg = input("Would you like for this query to be negated?(y/n) Note that negation only works for one-word/phrase "
                "queries and queries connected with AND: ")
    while neg != "y" and neg != "n":
        neg = input("Please type either 'y' or 'n': ")
    if neg == "y":
        first_neg = True
    else:
        first_neg = False
    check_if_more = input("Would you like to add a second part to your query? (y/n): ")
    while check_if_more != "y" and check_if_more != "n":
        check_if_more = input("Please type either 'y' or 'n': ")
    if check_if_more == "y":
        second_word = input("Please type your second query now: ").lower()
        neg = input("Would you like for this query to be negated?(y/n): ")
        while neg != "y" and neg != "n":
            neg = input("Please type either 'y' or 'n': ")
        if neg == "y":
            second_neg = True
        else:
            second_neg = False
        which_bool = input("Thanks! To find documents with either of these queries, please type 'OR'.\n To only find "
                           "documents with both, type 'AND': ")
        while which_bool != "OR" and which_bool != "AND":
            which_bool = input("Please type either 'OR' or 'AND' ")
        if which_bool == "AND":
            if not first_neg and not second_neg:
                if used_dictionary[first_word] != "no documents found" and used_dictionary[second_word] != "no documents found":
                    query_result = intersect(used_dictionary[first_word], used_dictionary[second_word])
                else:
                    query_result = []
            elif first_neg:
                first_word_neg = negation(first_word, used_dictionary, tokenized_doc_list)
                if used_dictionary[second_word] != "no documents found":
                    query_result = intersect(first_word_neg, used_dictionary[second_word])
                else:
                    query_result = []
            elif second_neg:
                second_word_neg = negation(second_word, used_dictionary, tokenized_doc_list)
                if used_dictionary[first_word] != "no documents found":
                    query_result = intersect(used_dictionary[first_word], second_word_neg)
                else:
                    query_result = []
            else:
                query_result = "no documents found"
            print("Your query matches the following documents: ", query_result)

        elif which_bool == "OR":
            if used_dictionary[first_word] != "no documents found" and used_dictionary[second_word] == "no documents found":
                query_result = used_dictionary[first_word]
            elif used_dictionary[first_word] == "no documents found" and used_dictionary[second_word] != "no documents found":
                query_result = used_dictionary[second_word]
            elif used_dictionary[first_word] != "no documents found" and used_dictionary[second_word] != "no documents found":
                query_result = union(used_dictionary[first_word], used_dictionary[second_word])
            else:
                query_result = "no documents found"
            print("Your query matches the following documents: ", query_result)
    else:
        if first_neg:
            matches = negation(first_word, used_dictionary, tokenized_doc_list)
            print("These are the documents that don't contain your search term/phrase: ", matches)
        else:
            print("Your query matches the following documents: ", used_dictionary[first_word])

    again = input("Would you like to make another search?(y/n) ")
    while again != "y" and again != "n":
        again = input("Please type either 'y' or 'n': ")
    if again == "y":
        main()
    else:
        print("Have a nice day!")


if __name__ == "__main__":
    main()






