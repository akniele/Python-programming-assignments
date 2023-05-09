import sys
from bubble_sort import bubble
from collections import defaultdict


def make_dictionary():

    #initializes dictionary
    my_dict = defaultdict(list)

    #open and read file line by line
    word_list = open('sv-utf8.txt', 'r', encoding="utf8")
    lines = word_list.readlines()
    word_list.close()

    #strips words of newline character, adds alphabetically sorted word to keys in dict,
    #and original word to values
    for word in lines:
        word = word.strip().lower()
        list_for_sorting = list(word)
        sorted_word = "".join(bubble(list_for_sorting))
        my_dict[sorted_word].append(word)

    return my_dict

        
#gets user input and reacts to it
def run_program(my_dict):
    user_input = sys.argv[1].lower()
    sorted_input = "".join(sorted(user_input))
    if sorted_input in my_dict.keys():
        if user_input in my_dict[sorted_input]:
            for value in my_dict[sorted_input]:
                if value != user_input:
                    print(value)

def main():
    new_dict = make_dictionary() #creates new dictionary
    again = run_program(new_dict) #runs the program

main()
