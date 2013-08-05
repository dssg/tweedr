#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
from SubProcessR import runSubProcess
from BleiCorpus import *


def sldaPipeLine(
    tweets,
    labels,
    labelOutput,
    tweetOutput,
    ):

    createCorpus(tweets, labels, labelOutput, tweetOutput)
    (topics, predictions, labels) = runSubProcess(0.7, tweetOutput,
            labelOutput)
    return (predictions, labels)


def outputJSON(tweets, predictions):

    for (i, tweet) in enumerate(tweets):
        predictions[i] = 
        print json.dumps({'text': tweet, 'label': predictions[i]},
                         separators=(',', ':'))
