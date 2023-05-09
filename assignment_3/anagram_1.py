from collections import defaultdict
from bubble_sort import bubble

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
    user_input = input("Type in a word! ").lower()
    sorted_input = "".join(sorted(user_input))
    if sorted_input in my_dict.keys():
        if user_input in my_dict[sorted_input]:
            for value in my_dict[sorted_input]:
                if len(my_dict[sorted_input]) == 1:
                    print("There are no anagrams of this word.")
                elif value != user_input:
                    print(value)
        else:
            print("This word is not in the dictionary.")

    else:
        print("This word is not in the dictionary.")
            

def main():
    new_input = run_program(new_dict) #runs the program

    again = input("Would you like to try again? ") #checks if user wants to try again
    while again != "yes" and again != "no":
        again = input("Would you like to try again? ")
    if again == "yes":
        main()
    elif again == "no":
        pass
    else:
        print("This shouldn't happen")
        
new_dict = make_dictionary() #creates new dictionary

main() #runs main
