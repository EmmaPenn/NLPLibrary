'''
Filename: apology_analysis.py

A file to analyze different apologies

Authors: Emma Penn, Imogen Slavin, Jessica Baumann
DS 3500 Fall 2024
Professor John Rachlin
'''

import os

from nlp import TEXT

def filenames(folder):
    text_files = []
    for file in os.listdir(folder):
        pathway = folder +"/" + file
        text_files.append(pathway)
    return text_files


def main():

    analysis = TEXT()

    files_to_read = filenames("apologies")


    for file in files_to_read:

        analysis.add_textfile(file)

    print(analysis.files)


if __name__ == "__main__":
    main()