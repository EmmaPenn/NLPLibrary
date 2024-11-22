'''
Filename: apology_analysis.py

A file to analyze different apologies

Authors: Emma Penn,
'''

import os

from nlp import TEXT

def filenames(folder):
    text_files = []
    for file in os.listdir("apologies"):
        pathway = "apologies/" + file
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