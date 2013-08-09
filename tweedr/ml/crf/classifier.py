import os
import tempfile
import crfsuite
from tweedr.ml.crf import ItemSequence
from tweedr.ml.classifier import ClassifierI
from tweedr.ml.features import crf_feature_functions, featurize

from itertools import izip

import logging
logger = logging.getLogger(__name__)


class CRF(ClassifierI):
    '''
    Doesn't fit entirely within the classifier paradigm, due to the hierarchy of data:
    Sentences have each token labeled, but each sentence is an individual entity.
    '''
    def __init__(self, algorithm='l2sgd', type_='crf1d'):
        self.trainer = crfsuite.Trainer()
        self.trainer.select(algorithm, type_)
        # default parameters:
        self.trainer.set('c2', '0.1')

    def fit(self, X, y):
        # For a CRF, X is an iterable of lists of lists of features (=strings)
        # and y is a list of list of token labels (=strings)
        for features_iter, labels in zip(X, y):
            items = ItemSequence(features_iter)
            self.trainer.append(items, tuple(labels), 0)

        self.model_filepath = tempfile.NamedTemporaryFile(delete=False).name
        self.trainer.train(self.model_filepath, -1)
        # persist to file and pull it back out.
        self.tagger = crfsuite.Tagger()
        self.tagger.open(self.model_filepath)

    def get_params(self, help=False):
        params = self.trainer.params()
        return dict((name, self.trainer.help(name) if help else self.trainer.get(name)) for name in params)

    def predict(self, X):
        y = []
        for features_iter in X:
            items = ItemSequence(features_iter)
            # just die if self.tagger has not been set
            self.tagger.set(items)
            # could also run self.probability() and self.marginal()
            # convert tuple (output of viterbi()) to list
            labels = list(self.tagger.viterbi())
            y.append(labels)
        return y

    def set_params(self, **params):
        for name, value in params.item():
            self.trainer.set(name, value)

    # additional fields below are not required by ClassifierI
    def save(self, model_filepath):
        logger.debug('Saving model to %s', model_filepath)
        # just die if self.model_filepath doesn't exist
        os.rename(self.model_filepath, model_filepath)
        self.model_filepath = model_filepath

    @classmethod
    def from_file(cls, model_filepath):
        '''If we are given a model_filepath that points to an existing file, use it.
        otherwise, create a temporary file to store the model because CRFSuite
        doesn't seem to allow us to create a tagger directly from a trained
        trainer object.'''
        # cls = CRF, obviously
        crf = cls()
        crf.tagger = crfsuite.Tagger()
        logger.debug('Loading existing model from %s', model_filepath)
        crf.tagger.open(model_filepath)
        crf.model_filepath = model_filepath

        return crf

    @classmethod
    def from_data(cls, data):
        '''
        data must be iterables of objects that support CRF-ready (byte strings)
        .tokens and .labels attributes.
        '''
        crf = cls()
        X_y = ((featurize(datum.tokens, crf_feature_functions), datum.labels) for datum in data)
        X, y = izip(*X_y)
        # X (and y) are iterables, by the way

        logger.debug('Fitting CRF')
        crf.fit(X, y)

        return crf
