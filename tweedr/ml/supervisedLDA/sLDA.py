#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from SubProcessR import *


def runSLDA(tweets, labels):

# Pre-Process Tweets and Labels Here?

    runTraining(tweets, labels)
    predictions = runStreaming(tweets)


def outputJSON(tweets, predictions):

    for (i, tweet) in enumerate(tweets):
        print json.dumps({'text': tweet, 'label': predictions[i]},
                         separators=(',', ':'))
