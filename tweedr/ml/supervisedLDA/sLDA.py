#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from SubProcessR import runStreaming, runTraining


def runSLDA(tweets, labels):

# Pre-Process Tweets and Labels Here?

    runTraining(tweets, labels)
    predictions = runStreaming(tweets)
    return predictions


def outputJSON(tweets, predictions):

    for (i, tweet) in enumerate(tweets):
        print json.dumps({'text': tweet, 'label': predictions[i]},
                         separators=(',', ':'))
