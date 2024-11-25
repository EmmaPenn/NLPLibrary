'''
apology_analysis.py: A file to analyze different apologies

Authors: Emma Penn, Imogen Slavin, Jessica Baumann
DS 3500 Fall 2024
Professor John Rachlin
'''
import os
import pandas as pd
from nlp import TEXT
from sankey import make_sankey
from collections import Counter

def filenames(folder):
    """Get all file paths in the folder."""
    text_files = []
    for file in os.listdir(folder):
        pathway = folder + "/" + file
        text_files.append(pathway)
    return text_files

def preprocess_text(analysis, stop_words, k=None, selected_words=None):
    """Preprocess text files to extract word frequencies."""
    all_word_counts = Counter()
    file_word_counts = {}

    for file, attributes in analysis.files.items():
        words = attributes["text"].split()
        word_counts = Counter(words)

        # Remove stop words
        word_counts = {word: count for word, count in word_counts.items() if word not in stop_words}

        # Update global word count
        all_word_counts.update(word_counts)

        # Store per-file word count
        file_word_counts[file] = word_counts

    # Determine the set of words to include
    if selected_words:
        final_words = set(selected_words)
    else:
        # Union of k most common words across texts
        final_words = set(dict(all_word_counts.most_common(k)).keys())

    return file_word_counts, final_words

def prepare_sankey_data(file_word_counts, final_words):
    """Prepare data for the Sankey diagram."""
    rows = []

    for file, word_counts in file_word_counts.items():
        for word in final_words:
            if word in word_counts:
                rows.append([file, word, word_counts[word]])

    return pd.DataFrame(rows, columns=["Source", "Target", "Value"])

def main():
    """Main function for apology analysis."""
    analysis = TEXT()
    files_to_read = filenames("apologies")

    for file in files_to_read:
        analysis.add_textfile(file)

    # Load stop words
    stop_words = set(analysis.load_text("stopwords.txt"))

    # Preprocess texts and get word frequencies
    file_word_counts, final_words = preprocess_text(analysis, stop_words, k=10)  # Example: top 10 words

    # Prepare data for Sankey
    sankey_data = prepare_sankey_data(file_word_counts, final_words)

    # Generate Sankey diagram
    make_sankey(
        df=sankey_data,
        lst=["Source", "Target"],
        vals="Value",
        thickness=20,
        pad=10
    )

    analysis.barplot(file_word_counts, k=10)

    analysis.sunburst(file_word_counts, k=10)

if __name__ == "__main__":
    main()
