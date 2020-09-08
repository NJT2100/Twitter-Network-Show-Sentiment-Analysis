# -*- coding: utf-8 -*-
"""
    This module takes reads in the text content of the input csv
    containing the tweets and calculates the sentiment using the 
    nltk module. The module returns an output file composed of each
    record from the input csv appended with 4 new columns representing
    the sentiment; 'neg', 'neu', 'pos', 'compound'.

    Example:
        $ python sentiment.py tweets.csv sentiment.csv

    Made for: EECS 4415 - Big Data Systems (York University EECS dept.)
    Original Author: Tony Le

"""
import numpy as np
import pandas as pd
import argparse
import time
import csv
import re
import os.path
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA

parser = argparse.ArgumentParser(description="Calculate sentiment of each tweet")
parser.add_argument("input_file")
parser.add_argument("output_file")
args = parser.parse_args()

file_input = args.input_file
file_output = args.output_file

new_column_names = [
        'category',
        'status_id',
        'in_reply_to_id',
        'user_id',
        'text',
        'language',
        'created_at',
        'location',
        'verified',
        'Association',
        'neg',
        'neu',
        'pos',
        'compound'
    ]

def main():
    start = time.time()

    # If output file does not exist, create it and provide it with the column names
    if not os.path.exists(file_output):
        with open(file_output, mode="w", newline='') as output:
            writer = csv.writer(output)
            writer.writerow(new_column_names)

    # Analyze the title of the show and make note of whether or not it is sentiment neutral
    neutral_title_mapping = {}
    with open('identifiers.csv', mode='r') as show_file:
        reader = csv.reader(show_file)
        for row in reader:
            show = row[0]
            sia = SIA()
            pol_score = sia.polarity_scores(show)
            # If show title isn't neutral, provide it with neutral one
            if float(pol_score['neu']) == 1.0:
                neutral_title_mapping[show] = True
            else:
                neutral_title_mapping[show] = False 

    # Read the input file in 10000 record sized chunks, and for each tweet
    # calculate the sentiment, and append the results to the output file
    with open(file_input, encoding="utf8") as csv_file, open(file_output, 'a', newline='') as output:
        writer = csv.writer(output)
        for data_chunk in pd.read_csv(csv_file, chunksize=10000):
            for record in data_chunk.itertuples(index=True, name='Pandas'):
                show = getattr(record, 'category')
                text = getattr(record, 'text')

                # Substitute placeholder for the title
                if neutral_title_mapping[show] == False:
                    text = re.sub(show.lower(), 'PLACEHOLDER', text)
                    print(show + ' ' + text)

                sia = SIA()
                results = sia.polarity_scores(text)
                columns = [
                    show,
                    getattr(record, 'status_id'),
                    getattr(record, 'in_reply_to_id'),
                    getattr(record, 'user_id'),
                    getattr(record, 'text'),
                    getattr(record, 'language'),
                    getattr(record, 'created_at'),
                    getattr(record, 'location'),
                    getattr(record, 'verified'),
                    "Strong"
                ]
                writer.writerow(columns + [results['neg'], results['neu'], results['pos'], results['compound']])

    end = time.time()
    print("Finished in %d seconds" % (end - start))

if __name__ == "__main__":
    main()
