# import os
import argparse
import logging
from colorama import Fore

from sklearn import cross_validation  # , metrics
# from sklearn.pipeline import Pipeline
# from sklearn.feature_extraction import text

from tweedr.lib.text import gloss
from tweedr.models import DBSession, TokenizedLabel  # , Label
from tweedr.ml import crf, print_metrics_summary, compare_labels
from tweedr.ml.features import crf_feature_functions, featurize

logger = logging.getLogger(__name__)

# logger.debug('%d labels', DBSession.query(Label).count())
# for label in DBSession.query(Label):
#     logger.debug('  %s = %s', label.id, label.text)


def evaluate(train, test, print_gloss=False):
    '''
    Train and test must be iterables of objects that support CRF-ready .tokens
    and .labels attributes.
    '''
    logger.info('Training on %d, testing on %d', len(train), len(test))
    tagger = crf.Tagger.from_path_or_data(train, crf_feature_functions)

    gold_labels = []
    predicted_labels = []
    for item in test:
        tokens = item.tokens
        item_gold_labels = item.labels
        gold_labels += item_gold_labels
        tokens_features = featurize(tokens, crf_feature_functions)
        item_predicted_labels = list(tagger.tag_raw(tokens_features))
        predicted_labels += item_predicted_labels

        if print_gloss:
            alignments = zip(tokens, item_gold_labels, item_predicted_labels)
            print '-' * 80
            print gloss(alignments,
                prefixes=(Fore.WHITE, Fore.YELLOW, Fore.BLUE),
                postfixes=(Fore.RESET, Fore.RESET, Fore.RESET))

    # sklearn metrics doesn't like string labels.
    used_labels = list(set(gold_labels + predicted_labels))
    print 'used_labels', used_labels
    lookup = dict((label, index) for index, label in enumerate(used_labels))
    print 'lookup', lookup
    # remap to integers
    gold_labels = [lookup[gold_label] for gold_label in gold_labels]
    predicted_labels = [lookup[predicted_label] for predicted_label in predicted_labels]

    print_metrics_summary(gold_labels, predicted_labels)
    # classification_report requires numeric labels, apparently?
    # print metrics.classification_report(gold_labels, predicted_labels)

    counts = compare_labels(gold_labels, predicted_labels, lookup['None'])
    print 'counts', counts
    precision = float(counts.true_positives) / (counts.true_positives + counts.false_positives)
    recall = float(counts.true_positives) / (counts.true_positives + counts.false_negatives)
    fscore = 2 * (precision * recall / (precision + recall))
    for name, value in [('Precision', precision), ('Recall', recall), ('F-score', fscore)]:
        print '%s: %.4f' % (name, value)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Train CRFSuite on data from the QCRI MySQL database',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-k', '--k-folds',
        type=int, default=10, help='How many folds of the data to test on')
    parser.add_argument('--max-data',
        type=int, default=10000, help='Maximum data points to train and test on')
    parser.add_argument('--crfsuite-version',
        action='store_true', help='Print the active crfsuite version')
    opts = parser.parse_args()

    if opts.crfsuite_version:
        print 'CRFSuite v%s' % crf.version
    else:
        # e.g., tokenized_label =
        # <TokenizedLabel dssg_id=23346 token_start=13 token_end=16
        #    tweet=Tornado Kills 89 in Missouri. http://t.co/IEuBas5 token_type=i18 token= 89 id=5>
        tokenized_labels = DBSession.query(TokenizedLabel).limit(opts.max_data).all()

        N = len(tokenized_labels)
        for train_indices, test_indices in cross_validation.KFold(N, opts.k_folds, shuffle=True):
            # train, test = tokenized_labels[train_indices], tokenized_labels[test_indices]
            train = [tokenized_labels[i] for i in train_indices]
            test = [tokenized_labels[i] for i in test_indices]
            evaluate(train, test)
