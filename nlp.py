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

        text = self.load_stop_words(text, stop_words)

        # sentiment = self.sentiment_analysis(text)
        file_identifier = file.split("/")[1]

        self.files[file_identifier] = text



    def load_text(self, filename, parser=None):
        # Register a text file with the library. The label is an optional label you’ll use in your
        # visualizations to identify the text

        text_list = []
        with open(filename, "r") as infile:
            for line in infile:
                line = line.split("\n")[0]
                text_list.append(line)
        return text_list

    def specific_punc(self, mark, text):
        total_speech = ""
        text.split(mark)
        for i in text:
            if i != mark:
                total_speech += i
        return total_speech

    def remove_punc(self, text):
        string = str(" ")
        string  = string.join(text)
        punc_marks = [".", ",", "!", ":", ";", "(", ")"]
        #  for mark in punc_marks:
           # text = text.replace(mark, "")
        return total



    def load_stop_words(self, text, stopfile):

        modified_text = []
        for i in text:
            if i not in stopfile:
                modified_text.append(i)

        return modified_text



  #  def wordcount_sankey(self, word_list=None, k=5):

   # def sentiment_analysis(self, text):

  #  def barplot(self):
    # bar plot - directed to the audience vs talking about themselves

  #  def sunburst_chart(self):
    # sunburst chart - sentiment, category, etc.