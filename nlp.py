'''
nlp.py: a library to analyze text

Authors: Emma Penn, Imogen Slavin, Jessica Baumann
DS 3500 Fall 2024
Professor John Rachlin
'''
import matplotlib.pyplot as plt
from collections import Counter
import plotly.express as px
from nlp_parser import txt_parser
from textblob import TextBlob
from textblob.sentiments import

class TEXT:

    def __init__(self):

        self.files = {}  # dictionary containing the speaker: values should be dictionaries containing word count, word Length, and sentiment
        self.stop_words = []

    def add_stop_words(self, stop_words_file):
        # add a global variable for the stop words that will be used for each text file

        with open(stop_words_file, "r") as infile:
            for line in infile:
                self.stop_words.append(line)


    def load_text(self, filename, parser = "txt_file"):
        # Register a text file with the library. The label is an optional label you’ll use in your
        # visualizations to identify the text

        if parser == "txt_file":
            text_information = txt_parser(filename)

            string = self.remove_punc(text_information["text"])
            text_information["text"] = self.load_stop_words(string, self.stop_words)

            text_information["sentiment"] = self.sentiment_analysis(text_information["text"])


            self.files[filename] = text_information


    def remove_punc(self, text):
        punc_marks = [".", "!", ",", ":", ";", "(", ")"]

        for mark in punc_marks:
              text = text.replace(mark, "")
        return text


    def load_stop_words(self, text, stopfile):
        for word in stopfile:
            text = text.replace(word, "")
        return text

    def sentiment_analysis(self, text):
        '''
        Made using the Textblob Library example for sentiment analysis
        https://textblob.readthedocs.io/en/dev/advanced_usage.html#sentiment-analyzers
        '''

        text_analysis = TextBlob(text, analyzer = NaiveBayesAnalyzer())
        return text_analysis.sentiment





    def barplot(self, file_word_counts, k=10):
        """
        Creates a bar plot with subplots for each text file, showing the frequency
        of the top k words in each file.
        """
        import matplotlib.pyplot as plt
        from collections import Counter

        num_files = len(file_word_counts)
        fig, axes = plt.subplots(nrows=num_files, ncols=1, figsize=(10, 5 * num_files), squeeze=False)

        for idx, (file_name, word_counts) in enumerate(file_word_counts.items()):
            # Get the top k words and their counts
            most_common_words = Counter(word_counts).most_common(k)
            words, counts = zip(*most_common_words) if most_common_words else ([], [])

            # Plot in the corresponding subplot
            ax = axes[idx, 0]
            ax.bar(words, counts, color="skyblue")
            ax.set_title(f"Top {k} Words in {file_name}")
            ax.set_ylabel("Frequency")
            ax.set_xlabel("Words")
            ax.set_xticks(range(len(words)))
            ax.set_xticklabels(words, rotation=45, ha="right")

        # Adjust layout
        plt.tight_layout()
        plt.show()


    def sunburst(self, file_word_counts, k=10):
        """
        Creates a sunburst chart showing word frequencies across all text files.
        Each file is a parent, and its words are children.
        """
        data = {"File": [], "Word": [], "Frequency": []}

        # Build hierarchical data
        for file_name, word_counts in file_word_counts.items():
            # Get top k words
            most_common_words = Counter(word_counts).most_common(k)
            for word, freq in most_common_words:
                data["File"].append(file_name)
                data["Word"].append(word)
                data["Frequency"].append(freq)

        # Create sunburst chart
        fig = px.sunburst(
            data,
            path=["File", "Word"],  # Hierarchical structure
            values="Frequency",  # Word frequencies determine segment sizes
            color="File",  # Different colors for each file
            title="Word Frequencies Across Text Files",
        )

        fig.update_traces(textinfo="label+percent entry")  # Show labels and percentages
        fig.show()