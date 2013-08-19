# import os
import argparse
from colorama import Fore

from sklearn import cross_validation  # , metrics
# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction import text

import pylab as pl
from tweedr.lib.text import gloss
from tweedr.models import DBSession, TokenizedLabel, Label
from tweedr.ml import compare_labels  # print_metrics_summary
from tweedr.ml.crf.classifier import CRF
from tweedr.ml.features import crf_feature_functions, featurize
from sklearn.metrics import confusion_matrix

import logging
logger = logging.getLogger(__name__)

flatMap = lambda iterable: map(list, iterable)

def evaluateSequenceClassifier(classifier, train_X, train_y, test_X, test_y, index, opts):
    '''If you use print_gloss, your test_y better be lists, not iterables.'''
    logger.info('Training on %d, testing on %d', len(train_y), len(test_y))
    classifier.fit(train_X, train_y)
    predicted_y = classifier.predict(test_X)
    # flatten
    test_y = sum(test_y, [])
    predicted_y = sum(predicted_y, [])
    #counts = compare_labels(test_y, predicted_y, 'None')

    gold_labels = []
    predicted_labels = []
    i = 0
    diction = {}

    j = 0

    while j < len(test_y):
        try:
            diction[test_y[j]] += 1
        except KeyError:
            diction[test_y[j]] = 1
        j = j + 1


    if (opts.include_none == 0):
        while i < len(test_y):
            if (test_y[i] == "None" and predicted_y[i] == "None"):
                pass
            else:
                try:
                    if diction[test_y[i]] > opts.threshold:                 
                        gold_labels.append(test_y[i])
                        predicted_labels.append(predicted_y[i])
                except KeyError:
                    pass
            i = i + 1
        
    cm = confusion_matrix(gold_labels, predicted_labels)
    print "Confusion Matrix"
    print cm
    pl.matshow(cm)
    pl.title('Confusion Matrix')
    pl.colorbar()
    pl.savefig("confusion_matrix" + str(index) + '.png', format='png')
    pl.clf()



def main():
    parser = argparse.ArgumentParser(
        description='Train CRFSuite on data from the QCRI MySQL database',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-k', '--k-folds',
        type=int, default=10, help='How many folds of the data to test on')
    parser.add_argument('--max-data',
        type=int, default=10000, help='Maximum data points to train and test on')
    parser.add_argument('--include-none', type=int, default=0, help='Include None in Confusion Matrix.')
    parser.add_argument('-threshold', type =int, default=10, help='Threshold for number of gold labels classified.')
    opts = parser.parse_args()

    # e.g., tokenized_label =
    # <TokenizedLabel dssg_id=23346 token_start=13 token_end=16
    #    tweet=Tornado Kills 89 in Missouri. http://t.co/IEuBas5 token_type=i18 token= 89 id=5>
    # Train and test must be iterables of objects that support CRF-ready
    # .tokens and .labels attributes.
    query = DBSession.query(TokenizedLabel).limit(opts.max_data)
    X_y = ((featurize(item.tokens, crf_feature_functions), item.labels) for item in query)
    # unzip and flatten into static list
    X, y = zip(*X_y)
    # we need to read X multiple times, so make sure it's all static
    X = map(flatMap, X)

    categories = dict((label.id, label.text) for label in DBSession.query(Label))
    print 'categories', categories

    N = len(y)
    index = 0;
    for train_indices, test_indices in cross_validation.KFold(N, opts.k_folds, shuffle=True):
        # train, test = tokenized_labels[train_indices], tokenized_labels[test_indices]
        train_X = [X[i] for i in train_indices]
        train_y = [y[i] for i in train_indices]
        test_X = [X[i] for i in test_indices]
        test_y = [y[i] for i in test_indices]
        classifier = CRF()
        # print_gloss=True
        index = index + 1
        evaluateSequenceClassifier(classifier, train_X, train_y, test_X, test_y, index, opts)

if __name__ == '__main__':
    main()
