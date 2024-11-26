'''
apology_analysis.py: A file to analyze different apologies

Authors: Emma Penn, Imogen Slavin, Jessica Baumann
DS 3500 Fall 2024
Professor John Rachlin
'''
import os
import pandas as pd
from nlp import TEXT
from collections import Counter

def filenames(folder):
    """Get all file paths in the folder."""
    text_files = []
    for file in os.listdir(folder):
        pathway = folder + "/" + file
        text_files.append(pathway)
    return text_files

def main():

    analysis = TEXT()
    analysis.add_stop_words('stopwords.txt')
    public_figures = filenames("public figures")
    politicians = filenames("politicians")
    corp_leaders = filenames("corporate leaders")

    for file in public_figures:
        analysis.load_text(file, category = "public figures")

    for file in politicians:
        analysis.load_text(file, category = "politicians")


    for file in corp_leaders:
        analysis.load_text(file, category = "corporate leaders")

    analysis.generate_sankey()

    analysis.barplot()

    analysis.sunburst(k=10)

    analysis.sentiment_plot(colors = ['midnightblue', 'forestgreen', 'fuchsia', 'steelblue'])

if __name__ == "__main__":
    main()