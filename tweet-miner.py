#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy

# API_KEY and API_SECRET
auth = tweepy.AppAuthHandler("1T8LHq0CqEWj3Ugpojj8YZasU", "LQHBu1mDkwUcwwAzLtFGE0HY1NCNbJZRji0CPRs4G32XHHvEQY")

api = tweepy.API(auth, wait_on_rate_limit=True,
                   wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

# Continue with rest of code

import argparse
import codecs
import time
import sys
import os

def twitter_miner(query, fName, since_id=0, max_id=-1):

    maxTweets = 500000 # An arbitrary large number
    searchQuery = query.encode('UTF-8')
    tweetCount = 0
    print("Downloading max {0} tweets".format(maxTweets))
    with codecs.open(fName, 'w') as f:
        while tweetCount < maxTweets:
            try:
                if (max_id <= 0):
                    if (not since_id):
                        new_tweets = api.search(q=searchQuery, count=100)
                    else:
                        new_tweets = api.search(q=searchQuery, count=100,
                                                since_id=since_id)
                else:
                    if (not since_id):
                        new_tweets = api.search(q=searchQuery, count=100,
                                                max_id=str(max_id - 1))
                    else:
                        new_tweets = api.search(q=searchQuery, count=100,
                                                max_id=str(max_id - 1),
                                                since_id=since_id)
                if not new_tweets:
                    print("No more tweets found")
                    break
                for tweet in new_tweets:
                    f.write((str(tweet.id) + '\t' + unicode(tweet.user.name) + '\t' + unicode(tweet.user.screen_name) + '\t' + ((tweet.text).replace('\n', ' ')) + '\n').encode('utf8'))
                tweetCount += len(new_tweets)
                print("Downloaded {0} tweets for query '{1}'".format(tweetCount, searchQuery))
                max_id = new_tweets[-1].id
            except tweepy.TweepError as e:
                # Just exit if any error
                print("some error : " + str(e))
                print("retrying in 20 seconds")
                time.sleep(20)
                continue

    print ("Downloaded {0} tweets for query {1}, Saved to {2}".format(tweetCount, searchQuery, fName))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(__file__, description="Collect all tweets for a given query and save them to a file")
    parser.add_argument("query", type=lambda s : unicode(s, sys.getfilesystemencoding()), help="The term to search for. The AND and OR operators can be used.")
    parser.add_argument("file", help="The name of the file to create and/or write over")
    parser.add_argument("--since_id", "-s", help="When retrieving tweets posted since a previous query was completed, insert the tweet_id from the top of the previous file after this flag", type=int, default=0)
    parser.add_argument("--max_id", "-m", help="If a search is interrupted, insert the tweet of the last tweet in the file after this flag to complete the search", type=int, default=-1)

    args = parser.parse_args()

    twitter_miner(args.query, args.file, args.since_id, args.max_id)