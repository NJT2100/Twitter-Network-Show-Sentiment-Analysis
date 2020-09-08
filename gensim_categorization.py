# -*- coding: utf-8 -*-
"""
    This module reads in the preprocessed output of categorization.py
    and analyzes the documents to determine which words are important.
    The most important wortds are interpreted through tf-idf analysis 
    and are then used to catgorize the Tweets which could not originally
    fitted into specific shows.

    Example:
        $ python gensim_categorization.py reference.csv

    Made for: EECS 4415 - Big Data Systems (York University EECS dept.)
    Original Author: Nathan Thomas

"""
import re
import sys
import csv
import time
import argparse
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from gensim.corpora import Dictionary
from gensim.models import TfidfModel
from gensim.corpora.textcorpus import TextCorpus
from gensim.test.utils import datapath
from gensim import utils 

parser = argparse.ArgumentParser(description="Clean the raw Tweets")
parser.add_argument("training_file")
args = parser.parse_args()

stop_words = set(stopwords.words('english'))

def generate_corpus(series, documents):
    """
        Create a corpus for a show 

        Args:
            series (string): The name of the show we want to build a corpus for.
                             Reads all documents if equals None
            documents (string): The name of the file which holds all the Tweets
        Returns:
            all_words list: <string>: A list of all the Tweets for a given show
    """
    all_words = []
    for data_chunk in pd.read_csv(documents, chunksize=10000):
        for record in data_chunk.itertuples(index=True, name='Pandas'):
            text = getattr(record, 'text')
            lang = getattr(record, 'language')
            words = text.split(" ")

            if lang == 'en':
                if series != None:
                    show = getattr(record, 'category')
                    if show == series:
                        all_words.append(words)
                if series == None:
                    all_words.append(words)
    
    return all_words

def generate_identifiers(training_file):
    """
        Find the highest ranked words among each show  

        Args:
            training_file (string): The name of the file holding the tweets
        Returns:
            all_words list: <string>: A list of all the Tweets for a given show
    """
    with open('identifiers.csv', mode='r') as identifier_file, open('new_identifiers.csv', mode='w', newline='') as new_identifier_file:
        reader = csv.reader(identifier_file, delimiter=',')
        for row in reader:
            show = row[0]

            # generate a corpus for only the desired show
            dataset = generate_corpus(show, training_file)

            dct = Dictionary(dataset)

            # Create a tfidf model to evaluate word rank
            corpus = [dct.doc2bow(line) for line in dataset]
            tfidf_model = TfidfModel(corpus)

            tfidf_freq = {}
            for doc in tfidf_model[corpus]:
                for id, freq in doc:
                    tfidf_freq[dct[id]] = freq
            
            tfidf_freq = sorted(tfidf_freq.items(), key=lambda x: x[1], reverse=True)

            for word, freq in tfidf_freq[:500]:
                print('%s, %s' % (word, freq), end='\n')

            writer = csv.writer(new_identifier_file, delimiter=',')
            keywords = []
            for word, freq in tfidf_freq[:10]:
                keywords.append(word)
            writer.writerow([show, ";".join(keywords)])
                
def main():
    start = time.time()
    
    generate_identifiers(args.training_file)

    end = time.time()
    print("Finished in %d seconds" % (end-start))

if __name__ == '__main__':
    main()