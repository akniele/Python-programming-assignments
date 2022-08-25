from nltk.tokenize import word_tokenize
from collections import defaultdict
import numpy as np


def create_vocabulary():
    """returns a list that contains all the words that
     occur in at least one of the documents, but no duplicates"""
    vocabulary = set()
    for doc in doc_list:
        my_file = open(doc, encoding="utf-8").read()
        words = word_tokenize(my_file)
        for word in words:
            if word.isalpha():
                vocabulary.add(word.lower())
    vocabulary = list(vocabulary)
    return vocabulary


def vocabulary_dict(vocabulary):
    """returns a dictionary that contains the vocabulary words as
     keys and their index in the vocabulary list as the corresponding value"""
    vocab_dict = defaultdict()
    for i, vocab in enumerate(vocabulary):
        vocab_dict[vocab] = i
    return vocab_dict


def term_frequency(vocab_dict):
    """returns a two-dimensional array in which each row represents a vocabulary
    word and each column a document. The individual cells represent how many times
    a specific word occurs in a specific document."""
    vocabulary = create_vocabulary()
    term_freq = np.zeros((len(vocabulary), len(doc_list)))
    for i, doc in enumerate(doc_list):
        my_file = open(doc, encoding="utf-8").read()
        words = word_tokenize(my_file)
        for word in words:
            if word.isalpha():
                term_freq[vocab_dict[word.lower()]][i] += 1
    return term_freq


def doc_frequency(term_freq):
    """returns a one-dimensional array the size of the vocabulary that tells us how
    many documents a certain word occurs in"""
    doc_freq = np.zeros(len(vocab_list), dtype="int")
    for i in range(len(doc_list)):
        for j in range(len(vocab_list)):
            if term_freq[j][i] != 0:
                doc_freq[j] += 1
    return doc_freq


def tf_idf(term_freq_array, doc_freq_array):
    """tf idf stands for ’term frequency - inverse document frequency’.
    The function returns an array that contains a weight for each word in each document.
    The value of the weight depends on both the term frequency of the word and the
    inverse document frequency"""
    weights = np.zeros((len(vocab_list), len(doc_list)))
    idf_list = np.zeros(len(vocab_list))
    for i in range(len(vocab_list)):
        if doc_freq_array[i] != 0:
            idf = np.log10(len(doc_list) / doc_freq_array[i])
        else:
            idf = 0
        idf_list[i] = idf
        for j in range(len(doc_list)):
            if term_freq_array[i][j] >= 1:
                tf = 1 + np.log10(term_freq_array[i][j])
            else:
                tf = 0
            weights[i][j] = tf * idf
    return weights, idf_list


def query_vector(query, idf_list, cosine_sim):
    """turns the user’s query into a vector. The vector consists of zeros except for
    at the indices that the words in the query have in the vocabulary list"""
    query_vec = np.zeros(len(vocab_list), dtype="int")

    for word in query:
        if word in vocabulary_dictionary:
            query_vec[vocabulary_dictionary[word]] += 1

    final_query_vec = query_vec * idf_list

    if not cosine_sim:
        final_query_vec[final_query_vec > 0] = 1
    return final_query_vec


def l2_norm(doc):
    """calculates the l2-norm of a vector (i.e. of the document)"""
    squared_doc = doc * doc
    summed_query = np.sum(squared_doc)
    normed_doc = np.sqrt(summed_query)
    return normed_doc


def cosine_similarity(k, weights, query_vec, cosine):
    """calculates the cosine similarity between the query vector and each
    document. It then returns a list of the five documents that are most
    similar to the query vector"""
    similarity = np.zeros(len(doc_list))
    if cosine:
        normed_query = l2_norm(query_vec)
    else:
        normed_query = np.ones(len(vocab_list), dtype="int")
    np.seterr(invalid='ignore')
    unit_query = query_vec / normed_query
    for i, doc in enumerate(doc_list):
        if cosine:
            normed_doc = l2_norm(weights[:, i])
        else:
            normed_doc = np.ones(len(vocab_list), dtype="int")
        unit_dot = weights[:, i] / normed_doc
        similarity[i] = np.dot(unit_query, unit_dot)

    similarity_list = []
    for i, element in enumerate(similarity):
        similarity_list.append((element, i))

    similarity_sorted = sorted(similarity_list, key=lambda tup: tup[0], reverse=True)
    similarity_sorted_k = similarity_sorted[:k]
    similar_index = [j for (i, j) in similarity_sorted_k if i != 0 and not np.isnan(i)]

    k_most_similar = []
    for i in similar_index:
        k_most_similar.append(doc_list[i])
    return k_most_similar


def check_if_more():
    """checks if the user wants to add more words to their query, is called
    in the main function"""
    check = input("Would you like to add another word to your query? (y/n): ")
    while check != "y" and check != "n":
        check = input("Please type either 'y' or 'n': ")
    if check == "y":
        word = input("Please type the next word now: ").lower()
        return word
    else:
        return None


def main():
    """deals with user input, finding out how many words the user wants
    to search for and whether they want to use cosine similarity or a
    non-normalized similarity metric. It then prints the document ids
    that match the user’s query and asks if the user would like to
    make another search"""
    query = []
    word = input("Please type the first word of your query: ").lower()
    query.append(word)

    word = check_if_more()

    while word is not None:
        query.append(word)
        word = check_if_more()

    which_similarity = input("Would you like to use cosine similarity?(y/n) ")
    while which_similarity != "y" and which_similarity != "n":
        which_similarity = input("Please type either 'y' or 'n': ")
    if which_similarity == "y":
        cosine_sim = True
    else:
        cosine_sim = False

    query_vec = query_vector(query, idf_list, cosine_sim)
    cos_sim = cosine_similarity(5, weights_array, query_vec, cosine_sim)

    if len(cos_sim) != 0:
        print("Thanks! The most relevant documents are: ", cos_sim)
    else:
        print("Unfortunately there are no documents that match your query. ")

    again = input("Would you like to make another search?(y/n) ")
    while again != "y" and again != "n":
        again = input("Please type either 'y' or 'n': ")
    if again == "y":
        main()
    else:
        print("Have a nice day!")


if __name__ == "__main__":
    doc_list = [f"docs{i + 1}.txt" for i in range(50)]  # list of file names

    vocab_list = create_vocabulary()
    vocabulary_dictionary = vocabulary_dict(vocab_list)
    term_freq_array = term_frequency(vocabulary_dictionary)
    doc_freq_array = doc_frequency(term_freq_array)
    weights_array, idf_list = tf_idf(term_freq_array, doc_freq_array)
    main()
