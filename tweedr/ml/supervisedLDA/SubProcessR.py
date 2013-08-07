#!/usr/bin/python
# -*- coding: utf-8 -*-

import pyper as pyr


def runSubProcess(cutoff, tweetFile, labelFile):
    r = pyr.R(use_numpy=True, use_pandas=True)
    vocab = tweetFile + '.vocab'
    r.assign('cutoff', cutoff)
    r.assign('tweetFile', tweetFile)
    r.assign('vocabFile', vocab)
    r.assign('labelFile', labelFile)

    r.run("source('sLDA.R')")
    predictions = r['predictions']
    trueLabels = r['Ytest']
    return (predictions, trueLabels)


def runStreaming(tweets):
    r = pyr.R(use_numpy=True, use_pandas=True)
    r.assign('tweets', tweets)

    r.run("source('sLDAStream.R')")
    predictions = r['predictions']
    return predictions


def runTraining(tweets, labels):
    r = pyr.R(use_numpy=True, use_pandas=True)
    r.assign('tweets', tweets)
    r.assign('labels', labels)

    r.run("source('sLDATrain.R')")
