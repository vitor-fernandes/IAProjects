import re
from collections import Counter
import string
from operator import itemgetter

regex = "[a-zA-ZçÇãÃõÕáÁéÉíÍóÓúÚâÂêÊîÎôÔûÛàÀ']+"

text_data = open('shakespeare.txt').read().lower()

regexed_text = re.findall(regex, text_data)
counted_data = Counter(regexed_text)

def bigram(text):
    last_word = text[-1]
    penult_word = text[-2]

    count_penult_word = counted_data[penult_word]
    count_last_penult = 0
    
    for i in range(len(regexed_text)):
        if((regexed_text[i] == penult_word) and (regexed_text[i+1] == last_word)):
            count_last_penult += 1

    probability = count_last_penult / count_penult_word  

    return probability

def trigram(text):
    last_word = text[-1]
    penult_word = text[-2]
    antipenult_word = text[-3]

    count_penult_antipenult = len(re.findall(antipenult_word + " " + penult_word, text_data))
    count_last_penult_antipenult = 0

    for i in range(len(regexed_text)):
        if((regexed_text[i] == antipenult_word) and (regexed_text[i+1] == penult_word) and (regexed_text[i+2] == last_word)):
            count_last_penult_antipenult += 1

    probability = count_last_penult_antipenult / count_penult_antipenult  

    return probability

def suggester(text, Kgram):

    print("Searching Suggestions Words...")
    print("It's can take a while, please wait")

    phrase_without_spaces = ""
    phrase_without_spaces_list = []
    for word in text:
        if(word.isalpha()):
            phrase_without_spaces += " " + word.lower()
            phrase_without_spaces_list.append(word.lower())

    phrase_without_spaces = phrase_without_spaces[1:]

    last_word = phrase_without_spaces_list[-1]
    penult_word = phrase_without_spaces_list[-2]

    post_last_word_words = []

    find_words = []
    
    if(Kgram == "B"):
        post_last_word_words = list(set(re.findall(last_word + " " + regex, text_data)))
        for w in post_last_word_words:
            word = w.split(' ')[1]
            phrase_N_word = (phrase_without_spaces + " " + word).split(' ')
            probability = bigram(phrase_N_word)
            find_words.append([word, probability])
    
    else:
        post_last_word_words = list(set(re.findall(penult_word + " " + last_word + " " + regex, text_data)))
        for w in post_last_word_words:
            word = w.split(' ')[2]
            phrase_N_word = (phrase_without_spaces + " " + word).split(' ')
            probability = trigram(phrase_N_word)
            find_words.append([word, probability])

    suggestions_words = sorted(find_words, key=itemgetter(1), reverse=True)[:3]
    suggestions_words_final = []

    final_phrases = []

    for word in suggestions_words:
        suggestions_words_final.append(word[0])
        final_phrases.append(phrase_without_spaces + " " + word[0])
    

    return(final_phrases, phrase_without_spaces, suggestions_words_final)

def formatter(result):
    print("Suggestion Words: {}".format(result[2]))
    print("Phrase with Suggestions: ")
    for phrase in result[0]:
        print(phrase)

def main():

    print("+============+")
    print("| SELECT ONE |")
    print("| 1- Bigram  |")
    print("| 2- Trigram |")
    print("| 3- Exit    |")
    print("+============+")
    print()
    Kgram = int(input("-> "))

    if(Kgram == 1):
        phrase = input("Type your Phrase: ").split(' ')
        formatter(suggester(phrase, "B"))

    elif(Kgram == 2):
        phrase = input("Type your Phrase: ").split(' ')
        formatter(suggester(phrase, "T"))

    elif(Kgram == 3):
        print("Bye !!!")
        
    else:
        print("Select a Number Between 1 - 3")

main()
