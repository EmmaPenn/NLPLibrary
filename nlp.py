'''
nlp.py: a library to analyze text

Jessica Baumann, Emma Penn, Imogen Slavin
DS3500 Fall 2024
Dr. Rachlin

'''
class TEXT:

    self.files = {} # dictionary containing the speaker: values should be dictionaries containing word count, word Length, and sentiment

    def __init__(self, file):
        text = self.load_text(file)

        text = self.load_stop_words(text)

        sentiment = self.sentiment_analysis(text)

        self.files[file] = [text, sentiment]


    def load_text(self, filename, label=””, parser=None):
# Register a text file with the library. The label is an optional label you’ll use in your
# visualizations to identify the text

    text_list = []
    with open(filename, "r") as infile:
        for line in infile:
            text_list.append(line)

    return text_list


    def load_stop_words(self, stopfile):


    def wordcount_sankey(self, word_list=None, k=5):

    def sentiment_analysis(self, text):

    def barplot(self):
    # bar plot - directed to the audience vs talking about themselves

    def sunburst_chart(self):
    # sunburst chart - sentiment, category, etc.