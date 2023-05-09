import random
from collections import defaultdict
import operator
from nltk import word_tokenize
from nltk import sent_tokenize


class AutoCorrect:
    def __init__(self, word_list, alpha):
        self.word_list = word_list
        self.alpha = alpha

#four methods for doing the Damerau–Levenshtein edit distance
    def insertion(self, word):
        list_of_similar_words = []
        for letter in self.alpha:
            wrd = list(word)
            for i in range(len(wrd)+1):
                wrd2 = wrd.copy()
                wrd2.insert(i, letter)
                vocab = ("").join(wrd2)
                if vocab in self.word_list:
                    list_of_similar_words.append(vocab)
        return list_of_similar_words
                    

    def deletion(self, word):
        list_of_similar_words = []
        wrd = list(word)
        for i, letter in enumerate(wrd):
            wrd1 = wrd.copy()
            del wrd1[i]
            vocab = ("").join(wrd1)
            if vocab in self.word_list:
                list_of_similar_words.append(vocab)
        return list_of_similar_words
                
            
    def substitution(self, word):
        list_of_similar_words = []
        for letter in self.alpha:
            wrd = list(word)
            for i in range(len(wrd)):
                wrd2 = wrd.copy()
                wrd2[i] = letter
                vocab = ("").join(wrd2)
                if vocab in self.word_list:
                    list_of_similar_words.append(vocab)
        return list_of_similar_words

   
    def swapping(self, word):
        list_of_similar_words = []
        list_word = list(word)
        for i in range(len(list_word)-1):
            copy_list_word = list_word.copy()
            copy_list_word[i], copy_list_word[i+1] = copy_list_word[i+1], copy_list_word[i]
            final_word = ("").join(copy_list_word)
            if final_word in self.word_list:
                list_of_similar_words.append(final_word)
        return list_of_similar_words
        
#uses the above edit distance methods to return a set of autocorrect-suggestions
    def final_autocorrect_set(self, word):
        final_list = self.insertion(word) + self.deletion(word) + self.substitution(word) + self.swapping(word)
        final_set = set(final_list)
        return final_set

#creates a bigram-frequency dictionary from the corpus file
def create_freq_dict():
    with open("corpus.txt", encoding = "utf-8") as f:
        bigram_frequency = defaultdict(int)
        for line in f:
            line_without_special_char = ''
            for character in line:
                if character not in options:
                    line_without_special_char += character

            token_words = word_tokenize(line_without_special_char)

            for i in range(len(token_words)-1):
                bigram = token_words[i], token_words[i+1]
                bigram_frequency[bigram] += 1
    return bigram_frequency

options = "()*.,;:"

#returns the three most common continuations of the input word
def three_most_common_continuations(word, my_dict):
    bigrams_with_word = {}
    for key in my_dict.keys():
        if key[0] == word:
            bigrams_with_word[key] = my_dict.get(key)
    final_dict = dict(sorted(bigrams_with_word.items(), key=operator.itemgetter(1),reverse=True))
    list_keys = list(final_dict)
    list_keys_3 = list_keys[:3]
    final_list = []
    for item in list_keys_3:
        final_list.append(item[1])
    return final_list
            
#the alphabet of the English language (plus the accented "é"
alphabet = "abcdefghijklmnopqrstuvwxyzé"


#extract English lexicon from file
with open("ukenglish.txt", encoding = 'latin-1') as lexicon:
    word_list = set()
    for line in lexicon:
        word = line.strip('\n').lower()
        word_list.add(word)


#deals with 
def check(word, my_dict):

    #If the word is NOT in the word list
    if word.lower() not in word_list:
        first_try = AutoCorrect(word_list, alphabet)
        first_final = first_try.final_autocorrect_set(word) #set with autocorrect suggestions
        final_3 = []
        for element in first_final: #reduce number of suggestions to max. three
            if len(final_3) < 3:
                final_3.append(element)
        #depending on the number of suggestions, print something different:
        if len(final_3) > 1:
            print("This word does not exist.\nHere are some suggestions: ")
        elif len(final_3) == 1:
            print("This word does not exist.\nHere is a suggestion: ")
        else:
            #if the word does not exist and there are no suggestions (because the edit distance to all words is > 1)
            print("This word does not exist.\n")
            user_input = input("Type '1' to enter a new word, or '2' to get some random suggestions: ")
            while user_input != "1" and user_input != "2":
                user_input = input("Type '1' to enter a new word, or '2' to get some random suggestions: ")
            if user_input == "1":
                main()
            else:
                sample = random.sample(tuple(word_list), 3)
                for samp in sample:
                    print(samp)
                user_input = input("Type the word you would like to choose: ")
                check(user_input, my_dict)
        #if the word does not exist but there are suggestions:
        print()
        for i in final_3:
            print(i)
            print()
        if len(final_3) > 1:
            user_input = input("Type '1' for your word to be printed, or '2' to use one of the suggestions: ")
            while user_input != "1" and user_input != "2":
                user_input = input("Type '1' for your word to be printed, or '2' to use one of the suggestions: ")
            if user_input == "1":
                print(word)
                main()
            else:
                user_input = input(f"Which of the suggestions ({final_3}) would you like to print? ")
                while user_input not in first_final:
                    user_input = input(f"Which of the suggestions ({final_3}) would you like to print? ")
                print(user_input)
                check(user_input, my_dict)
        elif len(final_3) == 1:
            user_input = input("Type '1' for your word to be printed, or '2' for the suggestion to be printed: ")
            while user_input != "1" and user_input != "2":
                user_input = input("Type '1' for your word to be printed, or '2' for the suggestion to be printed: ")
            if user_input == "1":
                print(word)
                main()
            else:
                print(final_3[0])
                check(final_3[0], my_dict)
              

    #If the word IS in the word list
    else:
        contin = three_most_common_continuations(word, my_dict) #get the three most common continuations from the bigram dictionary
        #If there ARE bigrams with the input as the first word:
        if len(contin) != 0:
            if len(contin) == 1:
                print("Here is a possible continuation: ")
            else:
                print("Here are some possible continuations: ")
            print()
            for con in contin:
                print(con)
            print()
            if len(contin) == 1:
                user_input = input("Type '1' to enter a new word, or '2' to use the suggestion: ")
            else:
                user_input = input("Type '1' to enter a new word, or '2' to use one of the suggestions: ")
            while user_input != "1" and user_input != "2":
                user_input = input("Type '1' to enter a new word, or '2' to use one of the suggestions: ")
            if user_input == "1":
                main()
            else:
                if len(contin) == 1:
                    print(contin[0])
                    check(contin[0], my_dict)
                else: 
                    user_input = input(f"Which of the suggestions ({contin}) would you like to print? ")
                    while user_input not in contin:
                        user_input = input(f"Which of the suggestions ({contin}) would you like to print? ")
                    print(user_input)
                    check(user_input, my_dict)
        #If there are NO any bigrams with the input as the first word:
        else:
            print("There are no suggested continuations for this word.")
            user_input = input("Type '1' to enter a new word, or '2' to get some random suggestions: ")
            while user_input != "1" and user_input != "2":
                user_input = input("Type '1' to enter a new word, or '2' to get some random suggestions: ")
            if user_input == "1":
                main()
            else:
                sample = random.sample(tuple(word_list), 3)
                for samp in sample:
                    print(samp)
                user_input = input("Type the word you would like to choose: ")
                check(user_input, my_dict)

#initialize dictionary
my_dict = create_freq_dict()

#call dictionary function, get user input and check it
def main():
    word_2_check = input("Please type a word: ")
    check(word_2_check, my_dict)

if __name__ == "__main__":
    main()
