'''
nlp.py: a library to analyze text

Authors: Emma Penn, Imogen Slavin, Jessica Baumann
DS 3500 Fall 2024
Professor John Rachlin
'''
import matplotlib.pyplot as plt
from collections import Counter
import plotly.express as px

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

   # def sentiment_analysis(self, text):

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