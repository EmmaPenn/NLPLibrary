

from collections import Counter


def txt_parser(filename):
    file  = open(filename)
    string = " "
    with open(filename, "r") as infile:
        for line in infile:
            line = line.split("\n")[0]
            for word in range(len(line)):
                string += line[word]
    words = string.split(" ")
    wc = Counter(words)
    num = len(words)
    return {"text": string, "word count": wc, "numwords": num}
