# -*- coding: utf-8 -*-
"""
    This module takes reads in the preprocessed output of preprocessing.py
    and determines which show each tweet belongs to. The module scans the
    tweets for relevant hashtags and key words which relate it to a show or
    shows and outputs two documents. Reference.csv which contains shows which 
    were successfully matched and Remainder.csv which contains the tweets
    that could not be matched.

    Example:
        $ python categorization.py clean_tweets.csv

    Made for: EECS 4415 - Big Data Systems (York University EECS dept.)
    Original Author: Nathan Thomas

"""
import sys
import time
import argparse
import os
import os.path
import csv 
import re
import pandas as pd

parser = argparse.ArgumentParser(description="Determine which show each tweet belongs to.")
parser.add_argument("filename")
args = parser.parse_args()

REFERENCE_FILE = 'Reference.csv'
REMAINDER_FILE = 'Remainder.csv'

def construct_reference_remainder_set(csv_file, identifier_file):
    defining_terms = {}
    # Construct a dictionary where the show is the key and the values
    # are lists of keywords to be used to parse the tweets
    with open(file=identifier_file, mode='r') as filter_file: 
        reader = csv.reader(filter_file, delimiter=',')
        for row in reader:
            keywords = row[1].split(';')
            defining_terms[row[0]] = keywords
    
    # Construct two .csv files, the first file is the tweets that are successfully sorted
    # into their respective shows, the second file is for tweets that could not be sorted
    with open(file=REFERENCE_FILE, mode='w', newline='') as referece_file, open(file=REMAINDER_FILE, mode='w', newline='') as remainder_file:
        # Every tweet added to reference.csv goes in this set
        reference_set = set()

        # Everys show seen gets added to this set
        total_set = set()

        writer = csv.writer(referece_file)
        writer.writerow(["category","status_id","in_reply_to_id","user_id","text","language","created_at","location","verified", "Association"])
        for data_chunk in pd.read_csv(csv_file, chunksize=10000):
            for record in data_chunk.itertuples(index=True, name='Pandas'):
                text = getattr(record, 'text')
                status_id = getattr(record, 'status_id')
                total_set.add(status_id)

                # For each show in the dictionary, check if one of the key words related to
                # the show in the identifiers listare in the tweet. Break when a key word is matched 
                # and continue through the dictionary to see if it also matches another show
                for show, identifiers in defining_terms.items():
                    for key in identifiers:
                        if key in str(text):
                            columns = [
                                show,
                                status_id,
                                getattr(record, 'in_reply_to_id'),
                                getattr(record, 'user_id'),
                                text,
                                getattr(record, 'language'),
                                getattr(record, 'created_at'),
                                getattr(record, 'location'),
                                getattr(record, 'verified'),
                                "Strong"]
                            writer.writerow(columns)
                            reference_set.add(status_id)
                            break

        # With simple set logic we calculate which tweets have not been handled yet
        remainder_set = total_set - reference_set

        writer = csv.writer(remainder_file)
        writer.writerow(["status_id","in_reply_to_id","user_id","text","language","created_at","location","verified"])
        for data_chunk in pd.read_csv(csv_file, chunksize=10000):
            for record in data_chunk.itertuples(index=True, name='Pandas'):
                status_id = getattr(record, 'status_id')
                if status_id in remainder_set:
                    columns = [
                        status_id,
                        getattr(record, 'in_reply_to_id'),
                        getattr(record, 'user_id'),
                        getattr(record, 'text'),
                        getattr(record, 'language'),
                        getattr(record, 'created_at'),
                        getattr(record, 'location'),
                        getattr(record, 'verified')]
                    writer.writerow(columns)

def main():
    start = time.time()

    construct_reference_remainder_set(args.filename, 'identifiers.csv')

    end = time.time()
    print("categorization finished in %d seconds" % (end-start))
if __name__ == '__main__':
    main()