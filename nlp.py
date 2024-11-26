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
from textblob.sentiments import PatternAnalyzer
from sankey import make_sankey
from functools import reduce
from collections import defaultdict
from heapq import nlargest
import pandas as pd
import plotly.graph_objects as go
from readability import Readability

class TEXT:

    def __init__(self):

        self.files = {}  # dictionary containing the speaker: values should be dictionaries containing word count, word Length, and sentiment
        self.stop_words = []

    def add_stop_words(self, stop_words_file):
        """add a global variable for the stop words that will be used for each text file"""

        with open(stop_words_file, "r") as infile:
            for line in infile:
                line = line.split("\n")[0]
                self.stop_words.append(line)


    def load_text(self, filename, category, parser = "txt_file"):
        """Registers a text file with the library"""

        if parser == "txt_file":
            text_information = txt_parser(filename)

            reading_text = Readability(text_information["text"]).ari()
            grade_score = Readability(text_information["text"]).flesch_kincaid()
            text_information["fk score"] = grade_score.score

            text_information["readability"] = reading_text.score


            string = self.remove_punc(text_information["text"])
            text_information["text"] = self.load_stop_words(string, self.stop_words)

            text_information["sentiment"] = self.sentiment_analysis(text_information["text"])

            text_information["category"] = category

            filename = filename.split('/')[1]
            self.files[filename] = text_information


    def remove_punc(self, text):
        """ removes punctuation from text"""
        punc_marks = [".", "!", ",", ":", ";", "(", ")", "-", "[", "]"]

        for mark in punc_marks:
              text = text.replace(mark, " ")
        return text


    def load_stop_words(self, text, stopfile):
        """ remove stop words from the text"""
        text = text.split(" ")
        total = ""

        words = [word for word in text if word not in stopfile]

        return ' '.join(words)

    def sentiment_analysis(self, text):
        """ sentiment analysis to get polarity and subjectivity made using the Textblob Library example
        for sentiment analysis https://textblob.readthedocs.io/en/dev/advanced_usage.html#sentiment-analyzers
        """

        text_analysis = TextBlob(text, analyzer = PatternAnalyzer())
        return text_analysis.sentiment

    def reducer(self, counts, word_list):
        """creates counts for each word in the list"""
        counts[word_list] += 1

        return counts


    def preprocess_text(self, k=10, selected_words=None):
        """Preprocess text files to extract word frequencies."""
        all_word_counts = Counter()
        file_word_counts = {}

        words = []
        for key, value in self.files.items():
            file_word_counts[key] = value['word count']
            for i in value['text'].split():
                words.append(i)

        if k is not None:
            counts = defaultdict(int)
            totals = dict(reduce(self.reducer, words, counts))

            top_words = nlargest(k, totals, totals.get)

        for file, attributes in self.files.items():
            words = attributes["text"].split()
            word_counts = Counter(words)

            file_word_counts[file] = word_counts

            if selected_words:
                final_words = set(selected_words)
            else:
                words = attributes["text"].split()
                word_counts = Counter(words)

                word_counts = {word: count for word, count in word_counts.items() if word in top_words}

                all_word_counts.update(word_counts)

                file_word_counts[file] = word_counts

        return file_word_counts, top_words

    def prepare_sankey_data(self, file_word_counts, final_words):
        """Prepare data for the Sankey diagram by making a DataFrame"""
        rows = []

        for file, word_counts in file_word_counts.items():
            for word in final_words:
                if word in word_counts:
                    standardized = word_counts[word]/len(word_counts)
                    rows.append([file, word, standardized])

        return pd.DataFrame(rows, columns=["Source", "Target", "Value"])

    def generate_sankey(self, k=None, selected_words=None):
        """Generates Sankey diagram"""

        file_word_counts, top_words = self.preprocess_text()
        sankey_data = self.prepare_sankey_data(file_word_counts, top_words)
        make_sankey(
            df=sankey_data,
            lst=["Source", "Target"],
            vals="Value",
            thickness=20,
            pad=10
        )

    def barplot(self, k=10):
        """ Creates a bar plot with subplots for each text file, showing the frequency
        of the top k words in each file.
        """
        file_word_counts, words = self.preprocess_text(k, selected_words=None)
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

    def sunburst(self, k=10):
        """
        Creates a sunburst chart showing word frequencies across all text files.
        Each file is a parent, and its words are children.
        """
        file_word_counts, words = self.preprocess_text(k, selected_words=None)
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
            path=["File", "Word"],
            values="Frequency",  # Word frequencies determine segment sizes
            color="File",  # Different colors for each file
            title="Word Frequencies Across Text Files",
        )

        fig.update_traces(textinfo="label+percent entry")  # Show labels and percentages
        fig.show()

    def get_dictionary(self, empty_dict, attribute):
        """ changes a dictionary to include an attribute for each category"""
        for file, attributes in self.files.items():
            if attributes["category"] in empty_dict.keys():
                 empty_dict[attributes["category"]].append(attributes[attribute])
            else:
                empty_dict[attributes["category"]] = []
                empty_dict[attributes["category"]].append(attributes[attribute])

        for key, value in empty_dict.items():
            empty_dict[key] = (sum(value) / len(value)) / 100
        return empty_dict

    def sentiment_plot(self, colors):
        """ creates a scatter plot with different sentiment attributes """
        total = {}

        category_polarity = {}

        for file, attributes in self.files.items():
            if attributes["category"] in category_polarity.keys():
                 category_polarity[attributes["category"]].append(attributes["sentiment"][0])
            else:
                category_polarity[attributes["category"]] = []
                category_polarity[attributes["category"]].append(attributes["sentiment"][0])


        category_subjectivity = {}

        for file, attributes in self.files.items():
            if attributes["category"] in category_subjectivity.keys():
                category_subjectivity[attributes["category"]].append(attributes["sentiment"][1])
            else:
                category_subjectivity[attributes["category"]] = []
                category_subjectivity[attributes["category"]].append(attributes["sentiment"][1])

        for key, value in category_polarity.items():
            category_polarity[key] = sum(value) / len(value)

        for key, value in category_subjectivity.items():
            category_subjectivity[key] = sum(value) / len(value)

        total["polarity"] = category_polarity

        total["subjectivity"] = category_subjectivity

        ari_dict = {}
        fk_dict = {}

        ari_dict = self.get_dictionary(ari_dict, "readability")
        fk_dict = self.get_dictionary(fk_dict, "fk score")
        total["ari readability"] = ari_dict
        total["flesch kincaid score"] = fk_dict
        fig = go.Figure()
        color_iter = 0
        for key, value in total.items():
            fig.add_trace(go.Scatter(
                x=list(value.values()),
                y=list(value.keys()),
                marker=dict(color=colors[color_iter],
                            size=12),
                mode="markers",
                name= key
            ))
            color_iter += 1

        fig.update_layout(title=dict(text='Complexity and Sentiment Comparison across Different Speaker Types'),
                          xaxis=dict(title=dict(text='Scaled Score')),
                          yaxis=dict(title=dict(text='Speaker Type')))
        fig.show()





