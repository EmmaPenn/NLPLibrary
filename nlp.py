'''
nlp.py: a library to analyze text

Jessica Baumann, Emma Penn, Imogen Slavin
DS3500 Fall 2024
Dr. Rachlin

'''
class TEXT:

    def __init__(self):

        self.files = {}  # dictionary containing the speaker: values should be dictionaries containing word count, word Length, and sentiment

    def add_textfile(self, file):

        text = self.load_text(file)

        stop_words = self.load_text("stopwords.txt")

        text = self.remove_punc(text)

        text, word_count = self.load_stop_words(text, stop_words)

        # sentiment = self.sentiment_analysis(text)
        file_identifier = file.split("/")[1]

        self.files[file_identifier] = {"text": text, "word count": word_count, "attributes": []}



    def load_text(self, filename, parser=None):
        # Register a text file with the library. The label is an optional label you’ll use in your
        # visualizations to identify the text

        text_list = []
        with open(filename, "r") as infile:
            for line in infile:
                line = line.split("\n")[0]
                text_list.append(line)
        return text_list



    def remove_punc(self, text):
        string = str(" ")
        string  = string.join(text)
        punc_marks = [".", ",", "!", ":", ";", "(", ")"]
        word  = ""
        for letter in range(len(string)):
            word += string[letter]

        for mark in punc_marks:
            word = word.replace(mark, "")
        return word

    def remove_word(self, word, stop_word):
        if word not in stop_word:
          return word

    def filter_nones(self, item):
        return item != None


    def load_stop_words(self, text, stopfile):
        text = text.split(" ")
        stopfile = [stopfile]*len(text)
        phrase_words_removed = list(map(self.remove_word,text, stopfile))
        phrase_words_removed = list(filter(self.filter_nones, phrase_words_removed))

        phrase = ""
        for word in range(len(phrase_words_removed)):
            phrase += phrase_words_removed[word].lower()
            phrase += " "
        return phrase, len(phrase_words_removed)


  #  def wordcount_sankey(self, word_list=None, k=5):

   # def sentiment_analysis(self, text):

  #  def barplot(self):
    # bar plot - directed to the audience vs talking about themselves

  #  def sunburst_chart(self):
    # sunburst chart - sentiment, category, etc.