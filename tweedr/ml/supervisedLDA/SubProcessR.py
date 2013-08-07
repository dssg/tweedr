#!/usr/bin/python
# -*- coding: utf-8 -*-

<<<<<<< HEAD
from pyper import R
=======
import pyper as pyr
>>>>>>> 246f9cdaa38305ba824588b4e8e2937022ef2e65


def runSubProcess(cutoff, tweetFile, labelFile):
    r = pyr.R(use_numpy=True, use_pandas=True)
    vocab = tweetFile + '.vocab'
    r.assign('cutoff', cutoff)
    r.assign('tweetFile', tweetFile)
    r.assign('vocabFile', vocab)
    r.assign('labelFile', labelFile)

    r.run("source('sLDA.R')")
    topics = r['Topics']
    predictions = r['predictions']
    trueLabels = r['Ytest']
    return (predictions, trueLabels)


def runStreaming(tweets):
<<<<<<< HEAD
    r = R(use_numpy=True, use_pandas=True)
    print "Testing"
=======
    r = pyr.R(use_numpy=True, use_pandas=True)
>>>>>>> 246f9cdaa38305ba824588b4e8e2937022ef2e65
    r.assign('tweets', tweets)
    r.run("source('sLDAStream.R)")
    predictions = r['predictions']
    return predictions


def runTraining(tweets, labels):
    r = pyr.R(use_numpy=True, use_pandas=True)
    r.assign('tweets', tweets)
    r.assign('labels', labels)

    r.run("source('sLDATrain.R')")

