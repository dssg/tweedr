# import os
import argparse
from colorama import Fore

from sklearn import cross_validation  # , metrics
# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction import text

from tweedr.lib.text import gloss
from tweedr.models import DBSession, TokenizedLabel
from tweedr.ml import compare_labels  # print_metrics_summary
from tweedr.ml.crf.classifier import CRF
from tweedr.ml.features import crf_feature_functions, featurize

import logging
logger = logging.getLogger(__name__)

flatMap = lambda iterable: map(list, iterable)


def evaluateSequenceClassifier(classifier, train_X, train_y, test_X, test_y, print_gloss=False):
    '''If you use print_gloss, your test_y better be lists, not iterables.'''
    logger.info('Training on %d, testing on %d', len(train_y), len(test_y))
    classifier.fit(train_X, train_y)
    predicted_y = classifier.predict(test_X)

    if print_gloss:
        for tokens_features, gold_labels, predicted_labels in zip(test_X, test_y, predicted_y):
            print '-' * 80
            # hope that the first feature string is the unigram!
            tokens = [token_features[0] for token_features in tokens_features]
            print gloss(zip(tokens, gold_labels, predicted_labels),
                prefixes=(Fore.WHITE, Fore.YELLOW, Fore.BLUE),
                postfixes=(Fore.RESET, Fore.RESET, Fore.RESET))

    # flatten
    test_y = sum(test_y, [])
    predicted_y = sum(predicted_y, [])
    counts = compare_labels(test_y, predicted_y, 'None')
    print 'counts', counts

    # sklearn metrics doesn't like string labels.
    # used_labels = list(set(gold_labels + predicted_labels))
    # print 'used_labels', used_labels
    # lookup = dict((label, index) for index, label in enumerate(used_labels))
    # print 'lookup', lookup
    # remap to integers
    # gold_labels = [lookup[gold_label] for gold_label in gold_labels]
    # predicted_labels = [lookup[predicted_label] for predicted_label in predicted_labels]

    # print_metrics_summary(gold_labels, predicted_labels)
    # classification_report requires numeric labels, apparently?
    # print metrics.classification_report(gold_labels, predicted_labels)

    precision = float(counts.true_positives) / (counts.true_positives + counts.false_positives)
    recall = float(counts.true_positives) / (counts.true_positives + counts.false_negatives)
    fscore = 2 * (precision * recall / (precision + recall))
    for name, value in [('Precision', precision), ('Recall', recall), ('F-score', fscore)]:
        print '%s: %.4f' % (name, value)


def main():
    parser = argparse.ArgumentParser(
        description='Train CRFSuite on data from the QCRI MySQL database',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-k', '--k-folds',
        type=int, default=10, help='How many folds of the data to test on')
    parser.add_argument('--max-data',
        type=int, default=10000, help='Maximum data points to train and test on')
    opts = parser.parse_args()

    # e.g., tokenized_label =
    # <TokenizedLabel dssg_id=23346 token_start=13 token_end=16
    #    tweet=Tornado Kills 89 in Missouri. http://t.co/IEuBas5 token_type=i18 token= 89 id=5>
    # Train and test must be iterables of objects that support CRF-ready
    # .tokens and .labels attributes.
    query = DBSession.query(TokenizedLabel).\
        filter(TokenizedLabel.tweet is not None).\
        filter(TokenizedLabel.tweet != '').\
        limit(opts.max_data)
    X_y = ((featurize(item.tokens, crf_feature_functions), item.labels) for item in query)
    # unzip and flatten into static list
    X, y = zip(*X_y)
    # we need to read X multiple times, so make sure it's all static
    X = map(flatMap, X)

    N = len(y)
    for train_indices, test_indices in cross_validation.KFold(N, opts.k_folds, shuffle=True):
        # train, test = tokenized_labels[train_indices], tokenized_labels[test_indices]
        train_X = [X[i] for i in train_indices]
        train_y = [y[i] for i in train_indices]
        test_X = [X[i] for i in test_indices]
        test_y = [y[i] for i in test_indices]
        classifier = CRF()
        # print_gloss=True
        evaluateSequenceClassifier(classifier, train_X, train_y, test_X, test_y)

if __name__ == '__main__':
    main()
