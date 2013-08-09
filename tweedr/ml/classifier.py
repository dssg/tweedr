'''I recommend emulating the scikit-learn interface, with or without
ClassifierI because fit and predict are more descriptive names than append_raw
and save, etc. In the CRF case, it's less transparent how to access the
underlying tagger/trainer but I think as long as it's following the sklearn
paradigm, an opaque wrapper is okay.
'''
from sklearn import base

import logging
logger = logging.getLogger(__name__)


class ClassifierI(base.ClassifierMixin):
    '''
    Interface to emulate sklearn classifiers.

    * `X`: an iterable of data points, each of which might be a point in many-dimensional space, a list of strings, etc.
    * `y`: an iterable of discrete labels, each of which may be a string, or a True/False value, or just an integer (not a float).
    '''
    def __init__(self, *args, **kw):
        pass

    def fit(self, X, y):
        '''Fit the model according to the given training data.'''
        raise NotImplementedError(__doc__)

    def fit_transform(self, X, y=None):
        '''Fit to some data, then transform it'''
        self.fit(X, y)
        return self.transform(X)

    def get_params(self, deep=False):
        '''Get parameters for the estimator'''
        raise NotImplementedError(__doc__)

    def predict(self, X):
        '''Predict class labels for samples in X.'''
        raise NotImplementedError(__doc__)

    # def score(self, X, y):
    #     '''Returns the mean accuracy on the given test data and labels.'''
    #     raise NotImplementedError(__doc__)

    def set_params(self, **params):
        '''Set the parameters of the estimator.'''
        raise NotImplementedError(__doc__)

    def transform(self, X, threshold=None):
        '''Reduce X to its most important features.'''
        raise NotImplementedError(__doc__)
