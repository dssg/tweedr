#!/usr/bin/python
# -*- coding: utf-8 -*-
from pyper import R
import os

class supervisedLDA():

    def __init__(self, dataFileName, alpha=1.0, numtopics=5, eta=0.1, logistic=True, lamda=1.0, e_iter=10, m_iter=4, variance=0.25):
        model_filename = "%s/model_%s.RDS" % (os.getcwd(), dataFileName)
        topic_filename = "%s/topics_%s.RDS" % (os.getcwd(), dataFileName)
        vocab_filename = "%s/vocabulary_%s.RDS" % (os.getcwd(), dataFileName)
        self.params = {
            "numtopics": numtopics,
            "alpha": alpha,
            "eta": eta,
            "logistic": logistic,
            "lambda": lamda,
            "e_iter": e_iter,
            "m_iter": m_iter,
            "variance": variance
            "dataFiles": dataFileName,
            "model_filename": model_filename,
            "topic_filename": topic_filename,
            "vocab_filename": vocab_filename
        }
        self.r = R(use_pandas=True, use_numpy=True)
        self.assign_R_params()

    def update_params(self, param_name, param_value):
        self.params[param_name] = param_value

    def assign_R_params(self):
        for (key, value) in self.params.iteritems():
            self.r.assign(key, value)

    def fit(self, documents, labels):
        self.r.assign("documents", documents)
        self.r.assign("labels", labels)
        self.r.run('source("trainLDA.R")')
        topics = self.r["topics"]
        vocab = self.r["vocabulary"]
        self.update_params("topics", topics)
        self.update_params("vocab", vocab)
        self.assign_R_params()

    def predict(self, documents):
        self.r.assign("testDocuments", documents)
        self.r.run('source("testLDA.R")')
        predictions = self.r["predictions"]
        return predictions

    def save_model(self):
        self.r.run('source("saveModel.R")')

    def load_model(self):
        self.r.run('source("loadModel.R")')
        vocab = self.r["vocab"]
        topics = self.r["topics"]
        self.update_params("vocab", vocab)
        self.update_params("topics", topics)
        self.assign_R_params()

    def set_Data(self, documents, labels):
        self.update_params("documents", documents)
        self.update_params("labels", labels)
        self.assign_R_params()
