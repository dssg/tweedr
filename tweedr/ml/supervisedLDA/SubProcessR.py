#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyper import *
import numpy as np
import pandas as pd


def runSubProcess(cutoff, tweetFile, labelFile):
    r = R(use_numpy=True, use_pandas=True)
    vocab = tweetFile + '.vocab'
    r.assign('cutoff', cutoff)
    r.assign('tweetFile', tweetFile)
    r.assign('vocabFile', vocab)
    r.assign('labelFile', labelFile)

    r.run("source('sLDA.R')")
    topics = r['Topics']
    predictions = r['predictions']
    trueLabels = r['Ytest']
    return (topics, predictions, trueLabels)


def runStreaming(tweets):
    r = R(use_numpy=True, use_pandas=True)
    r.assign('tweets', tweets)
    r.run("source('sLDAStream.R)")
    predictions = r['predictions']
    return predictions


def runTraining(tweets, labels):
    r = R(use_numpy=True, use_pandas=True)
    r.assign('tweets', tweets)
    r.assign('labels', labels)

    r.run("source('sLDATrain.R')")
