#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from SubProcessR import runStreaming, runTraining
<<<<<<< HEAD
from PreProcess import processTweet, is_ascii
import csv
=======
>>>>>>> 246f9cdaa38305ba824588b4e8e2937022ef2e65


def runSLDA(tweets, labels):

# Pre-Process Tweets and Labels Here?

    tweets = map(lambda x: processTweet(x), tweets)
    tweets = [(tweet if is_ascii(tweet) else ' ') for tweet in tweets]
    tweets = map(lambda x: str(x).translate(None, '"'), tweets)
    tweets_filters, labels_filters = ([],[])
    for (i, tweet) in enumerate(tweets):
        if len(tweet) > 1:
            tweets_filters.append(tweet)
            labels_filters.appedn(labels[i])

    runTraining(tweets_filters, labels_filters)
    predictions = runStreaming(tweets_filters)
    return predictions

def outputJSON(tweets, predictions):

    for (i, tweet) in enumerate(tweets):
        print json.dumps({'text': tweet, 'label': predictions[i]},
                         separators=(',', ':'))
