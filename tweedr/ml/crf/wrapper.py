import os
import crfsuite
import tempfile

from tweedr.ml.crf import ItemSequence
from tweedr.ml.features import featurize

import logging
logger = logging.getLogger(__name__)


class Trainer(crfsuite.Trainer):
    """
    Inherit crfsuite.Trainer to implement message() function, which receives
    progress messages from a training process.
    """
    def message(self, s):
        logger.silly('Trainer.message: %s', s.strip())

    def append_raw(self, features_iter, labels):
        # len(labels) = len(features_iter) = length of sentence / sequence
        # labels is a tuple of strings, features_iter is an tuple/list of variable-length lists of strings.
        # this just wraps all the data / labels with crfsuite types
        items = ItemSequence(features_iter)
        # labels = crfsuite.StringList(labels)
        self.append(items, tuple(labels), 0)

    def save(self, model_path):
        # Trainer.select(algorithm, type): Initialize the training algorithm and set type of graphical model
        # lbfgs is the default algorithm
        # l2sgd is L2-regularized SGD
        # crf1d is 1st-order dyad features.
        self.select('l2sgd', 'crf1d')

        # Set the coefficient for L2 regularization to 0.1
        # potential values change based on algorithm previously selected
        # See http://www.chokkan.org/software/crfsuite/manual.html
        self.set('c2', '0.1')

        # Start training; the training process will invoke trainer.message()
        # to report the progress.
        self.train(model_path, -1)

        # print 'After training: params and their values'
        # for name in trainer.params():
        #     print name, trainer.get(name), trainer.help(name)


class Tagger(crfsuite.Tagger):
    def __init__(self, model_path):
        super(Tagger, self).__init__()
        self.open(model_path)

    def tag_raw(self, features_iter):
        '''
        Obtain the label sequence predicted by the tagger.

        This returns a tuple of strings (label identifiers)
        '''
        items = ItemSequence(features_iter)
        self.set(items)
        # could also run self.probability() and self.marginal()
        return self.viterbi()

    @classmethod
    def from_path_or_data(cls, data, feature_functions, model_filepath=None):
        '''If we are given a model_filepath that points to an existing file, use it.
        otherwise, create a temporary file to store the model because CRFSuite
        doesn't seem to allow us to create a tagger directly from a trained
        trainer object.'''
        if model_filepath is None or not os.path.exists(model_filepath):
            if model_filepath is None:
                model_filepath = tempfile.NamedTemporaryFile(delete=False).name

            trainer = Trainer()
            for i, datum in enumerate(data):
                tokens = datum.tokens
                labels = datum.labels

                tokens_features = featurize(tokens, feature_functions)
                trainer.append_raw(tokens_features, labels)

            trainer.save(model_filepath)
            logger.debug('Trained on %d instances and saved to %s', i, model_filepath)
        else:
            logger.debug('Loading existing model from %s', model_filepath)

        return cls(model_filepath)
