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


def main():
    """Main function for apology analysis."""
    analysis = TEXT()
    analysis.add_stop_words('stopwords.txt')
    files_to_read = filenames("apologies")

    print(analysis.stop_words)

    for file in files_to_read:
        analysis.load_text(file)

    print(analysis.files)

    analysis.generate_sankey()

    analysis.barplot()

    analysis.sunburst(k=10)

if __name__ == "__main__":
    main()