#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from SubProcessR import runStreaming, runTraining
import PreProcess


def runSLDA(tweets, labels):

# Pre-Process Tweets and Labels Here?

    tweets = map(lambda x: PreProcess.processTweet(x), tweets)
    tweets = [(tweet if PreProcess.is_ascii(tweet) else ' ')
              for tweet in tweets]
    tweets = map(lambda x: str(x).translate(None, '"'), tweets)
    (tweets_filters, labels_filters) = ([], [])
    myFile = open('dumpTweets.csv', 'wb')
    for (i, tweet) in enumerate(tweets):
        if len(tweet) > 1:
            tweets_filters.append(tweet)
            labels_filters.append(labels[i])
            myFile.write('"%s"\t%d\n' % (tweet, labels[i]))

    cutoff = int(round(0.8*len(tweets_filters)))
    runTraining(tweets_filters[:cutoff], labels_filters[:cutoff])
    print 'Done Training'
    predictions = runStreaming(tweets_filters[cutoff:])
    return (predictions, labels_filters[cutoff:])


def outputJSON(tweets, predictions):

    for (i, tweet) in enumerate(tweets):
        print json.dumps({'text': tweet, 'label': predictions[i]},
                         separators=(',', ':'))
