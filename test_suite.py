import info_retrieval


def words_only_once(token_dict):
    words_only_one_doc = []
    for key, value in token_dict.items():
        if len(value) <= 1:
            words_only_one_doc.append(key)
    return words_only_one_doc


def bigrams_only_once(bigram_dict):
    bigrams_only_once_doc = []
    for key, value in bigram_dict.items():
        if len(value) <= 1:
            bigrams_only_once_doc.append(key)
    return bigrams_only_once_doc

# To test the program, we first create a list of words and bigrams that only appear once:


words_one_file = words_only_once(info_retrieval.dictionary_of_tokens)
bigrams_one_file = bigrams_only_once(info_retrieval.dictionary_of_bigrams)

# We then choose some words and phrases that only occur in one document:

word_list = words_one_file[100:105]
for i, word in enumerate(word_list):
    print(f"word {i+1}: {word}")

bigram_list = bigrams_one_file[100:105]
for i, bigram in enumerate(bigram_list):
    print(f"bigram {i+1}: {bigram}")

# Now we can run info_retrieval.py and to see if these words/phrases indeed only occur in one document each.

