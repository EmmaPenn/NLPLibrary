'''
nlp_parser.py:

Authors: Emma Penn, Imogen Slavin, Jessica Baumann
DS 3500 Fall 2024
Professor John Rachlin

'''

from collections import Counter

def txt_parser(filename):
    file  = open(filename)
    string = " "
    with open(filename, "r") as infile:
        for line in infile:
            line = line.split("\n")[0]
            for word in range(len(line)):
                string += line[word].lower()
                #string += " "
    words = string.split(" ")
    wc = Counter(words)
    num = len(words)
    return {"text": string, "word count": wc, "numwords": num}
