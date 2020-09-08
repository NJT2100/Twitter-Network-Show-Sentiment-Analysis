# -*- coding: utf-8 -*-
"""
    This module connects to the Twitter using the official Twitter
    streaming API Tweepy and streams tweets. When a tweets is received 
    it is written to a .csv file along with relevant metadata related.
    Module is designed to simply be left running for long periods of time
    until a keyboard interupt is captured.

    Example:
        $ python twitter_stream.py tweets.csv

    Note:
        requires Twitter developer credentials to run. JSON of credentials
        read in .config file

    Made for: EECS 4415 - Big Data Systems (York University EECS dept.)
    Original Author: Nathan Thomas

"""
import sys
import os.path
import json
import csv 
import re
import argparse
import tweepy
import preprocessor as p

parser = argparse.ArgumentParser(description="Stream the raw Tweets")
parser.add_argument("output_file")
args = parser.parse_args()

TWITTER_FILE = args.output_file

class TwitterStreamListener(tweepy.StreamListener):
    """ 
        Extend StreamListener and define the on_status and on_error functions
    """

    def on_status(self, status):
        """
            On status append the tweet and the metadata to a .csv file

            Args:
                status (obj): An object holding the data related to the tweet
            Returns:
                void: writes a record of the tweet to disk
        """
        with open(TWITTER_FILE, mode="a+", newline='') as tweet_file:
            columnns = [
                status.id,
                status.in_reply_to_user_id,
                status.user.id,
                clean_tweet(status.text),
                status.lang,
                status.created_at,
                str(status.user.location).encode('raw_unicode_escape'),
                status.user.verified
            ]

            print(columnns)
            writer = csv.writer(tweet_file)
            writer.writerow(columnns)
	
    def on_error(self, status):
	    print(status)

class TwitterClient():
    """
        Create a class to initialize connection with Twitter
    """

    def __init__(self):
        """
            On creation, load credentials and authenticate self to Tweepy
        """
        with open(".config", "r") as config_file:
            credentials = json.loads(config_file.read())
            api_key = credentials["api_key"]
            api_secret = credentials["api_secret"]
            access_key = credentials["access_token"]
            access_secret = credentials["access_secret"]
        
        self.auth = tweepy.OAuthHandler(api_key, api_secret)
        self.auth.set_access_token(access_key, access_secret) 
        self.api = tweepy.API(self.auth)

def clean_tweet(status):
    """
        Remove urls, emoji, and smileys from tweet
    """
    p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.SMILEY)
    return p.clean(status).encode('raw_unicode_escape')

def main():
    filters = []
    with open("keywords.txt", mode="r") as filter_file:
        for key in filter_file:
            filters.append(str(key))
    
    column_names = [
        'status_id',
        'in_reply_to_id',
        'user_id',
        'text',
        'language',
        'created_at',
        'location',
        'verified'
    ]

    lang = [
        "en",
        "fr",
        "es",
        "ja",
        "ru",
        "pt",
        "sw"
    ]

    if os.path.exists(TWITTER_FILE) == False:
        with open("tweets.csv", mode="a+", newline='') as tweet_file:
            writer = csv.writer(tweet_file)
            writer.writerow(column_names)

    client = TwitterClient()
    tweetStreamListner = TwitterStreamListener()
    try:
        tweetStream = tweepy.Stream(auth = client.api.auth, listener=tweetStreamListner, tweet_mode='extended')    
        tweetStream.filter(track=filters, languages=lang)
    except tweepy.TweepError as e:
        print(e.reason)

    main()

if __name__ == "__main__":
    main()