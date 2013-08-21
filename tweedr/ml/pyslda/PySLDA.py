#!/usr/bin/python
# -*- coding: utf-8 -*-

from pyper import R
import os
from PreProcess import processTweet, is_ascii


class supervisedLDA:

    def __init__(self, dataFileName, alpha=1.0, numtopics=5, eta=0.1, logistic=True, lamda=1.0, e_iter=10, m_iter=4, variance=0.25, cutoff=0.25):
        model_filename = 'model_%s.RDS' % dataFileName
        vocab_filename = 'vocabulary_%s.RDS' % dataFileName
        fullpath = os.path.realpath(__file__)
        (path, files) = os.path.split(fullpath)
        self.path = path
        self.params = {
            'numtopics': numtopics,
            'alpha': alpha,
            'eta': eta,
            'logistic': logistic,
            'lambda': lamda,
            'e_iter': e_iter,
            'm_iter': m_iter,
            'variance': variance,
            'OutputName': dataFileName,
            'model_filename': model_filename,
            'vocab_filename': vocab_filename,
            'test_cutoff': cutoff,
        }
        self.r = R(use_pandas=True, use_numpy=True)
        self.assign_R_params()

    def set_param(self, param_name, param_value):
        self.params[param_name] = param_value

    def get_params(self, deep=False):
        return self.params

    def assign_R_params(self):
        for (key, value) in self.params.iteritems():
            self.r.assign(key, value)

    def fit(self, documents, labels):
        (documents, labels) = self.transform(documents, labels)
        self.r.assign('documents', documents)
        self.r.assign('labels', labels)
        self.r.run('source("trainLDA.R")')
        vocab = self.r['vocabulary']
        self.set_param('vocabulary', vocab)
        self.assign_R_params()

    def transform(self, documents, labels):
        documents = [(tweet if is_ascii(tweet) else ' ') for tweet in
                     documents]
        documents = map(lambda x: processTweet(x), documents)
        documents = map(lambda x: str(x).translate(None, '"'),
                        documents)
        (tweets_filtered, labels_filtered) = ([], [])
        for (tweet, label) in zip(documents, labels):
            if len(tweet) > 1:
                tweets_filtered.append(tweet)
                labels_filtered.append(label)
        return (tweets_filtered, labels_filtered)

    def test_transform(self, documents):
        documents = [(tweet if is_ascii(tweet) else ' ') for tweet in
                     documents]
        documents = map(lambda x: processTweet(x), documents)
        documents = map(lambda x: str(x).translate(None, '"'),
                        documents)
        tweets_filtered = []
        for tweet in documents:
            if len(tweet) > 1:
                tweets_filtered.append(tweet)
        return tweets_filtered

    def __str__(self):
        return 'sLDA(cut:%s)' % self.params['test_cutoff']

    def predict(self, documents, gold_labels):
        (documents, gold_labels) = self.transform(documents,
                gold_labels)
        self.r.assign('testDocuments', documents)
        self.r.run('source("testLDA.R")')
        predictions = self.r['pred']
        cutoff = self.params['test_cutoff']
        predictions = map(lambda x: int(x > cutoff), predictions)
        return (predictions, gold_labels)

    def save_model(self):
        self.r.run('source("%s/saveModel.R")' % self.path)

    def load_model(self):
        self.r.run('source("%s/loadModel.R")' % self.path)
        vocab = self.r['vocab']
        topics = self.r['topics']
        self.set_param('vocab', vocab)
        self.set_param('topics', topics)
        self.assign_R_params()
