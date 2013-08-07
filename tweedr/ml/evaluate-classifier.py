"""Evaluate the tweet classifier: is this tweet about damage/casualty or not?"""
# import os
import argparse
import logging
import numpy as np
from colorama import Fore

from sklearn import cross_validation  # , metrics
# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction import text

from tweedr.lib.text import gloss
from tweedr.models import DamageClassification, DBSession
from tweedr.ml import classifier, print_metrics_summary, compare_labels
from tweedr.ml.features import classifier_feature_functions, featurize

logger = logging.getLogger(__name__)


def evaluate(train, test, print_gloss=False):
    '''
    Train and test must be iterables of objects that support classifier-ready .tokens
    and .labels attributes.
    '''
    logger.info('Training on %d, testing on %d', len(train), len(test))
    #the_classifier = classifier.Classifier.from_path_or_data(train, classifier_feature_functions)
    #assert the_classifier
    # print_metrics_summary(gold_labels, predicted_labels)
    # print metrics.classification_report(gold_labels, predicted_labels)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Train a classifier on data from the QCRI MySQL database',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-k', '--k-folds',
        type=int, default=10, help='How many folds of the data to test on')
    parser.add_argument('--max-data',
        type=int, default=100, help='Maximum data points to train and test on')
    opts = parser.parse_args()

    labeled_tweets = np.array(DBSession.query(DamageClassification).limit(opts.max_data).all())
    N = len(labeled_tweets)
    logger.info('Read %d tweets from database', N)

    for train_indices, test_indices in cross_validation.KFold(N, opts.k_folds, shuffle=True):
        evaluate(labeled_tweets[train_indices], labeled_tweets[test_indices])
