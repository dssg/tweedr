"""Evaluate the tweet classifier: is this tweet about damage/casualty or not?

Results as of 8/8/13:

INFO:eval-clf:Reading labeled tweets from database...
INFO:eval-clf:Read 1045 tweets
model        	f1	   pre	rec	acc	f1_std pre_std	rec_std	acc_std
KNeighborsCla	0.52	0.84	0.38	0.84	0.09	 0.10	   0.08	   0.04
SVC(C=1, cach	0.45	0.89	0.32	0.83	0.14	 0.07	   0.13	   0.05
DecisionTreeC	0.55	0.91	0.40	0.85	0.09	 0.07	   0.08	   0.03
MultinomialNB	0.62	0.53	0.74	0.79	0.07	 0.08	   0.08	   0.03
LogisticRegre	0.66	0.78	0.59	0.86	0.05	 0.10	   0.06	   0.03
"""

import argparse
import logging
import numpy as np

from sklearn import cross_validation  # , metrics
from sklearn.feature_extraction.text import CountVectorizer
#from sklearn.feature_extraction.text import TfidfTransformer
from sklearn import metrics
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import MultinomialNB

from tweedr.models import DamageClassification, DBSession
#from tweedr.ml.pyslda import PySLDA

logger = logging.getLogger('eval-clf')


def summarize(evals, n):
    'Compute average and standard deviation for evaluation metrics'
    avg = {}
    for key in evals[0].iterkeys():
        scores = np.array([e[key] for e in evals])
        avg[key] = np.average(scores)
        avg[key + '_std'] = np.std(scores)
    return avg


def score(y_true, y_pred):
    '''Compute evaluation metrics. Note pos_label=1 parameter of
    f1/precision/recall. Thus, we only compute precision of the positive class
    (as opposed to computing the precision for both classes and taking the
    average).'''
    return {'acc': metrics.accuracy_score(y_true, y_pred),
            'f1': metrics.f1_score(y_true, y_pred, pos_label=1),
            'pre': metrics.precision_score(y_true, y_pred, pos_label=1),
            'rec': metrics.recall_score(y_true, y_pred, pos_label=1)}


def read_tweets():
    'Read labeled tweets from database'
    logger.info('Reading labeled tweets from database...')
    labeled_tweets = np.array(DBSession.query(DamageClassification).filter(DamageClassification.mturk_code == 'QCRI').limit(opts.max_data).all())
    logger.info('Read %d tweets', len(labeled_tweets))
    return labeled_tweets


def metric_names():
    'Name of metrics. Gotcha: keep in sync with score function'
    metric_names = ['f1', 'pre', 'rec', 'acc']
    return metric_names + [m + '_std' for m in metric_names]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Train a classifier on data from the QCRI MySQL database',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-k', '--k-folds',
        type=int, default=10, help='How many folds of the data to test on')
    parser.add_argument('--max-data',
        type=int, default=10000, help='Maximum data points to train and test on')
    opts = parser.parse_args()

    labeled_tweets = read_tweets()

    # FIXME: add features beyond bag of words
    pipeline = Pipeline([('vect', CountVectorizer())])
    #,                         ('tfidf', TfidfTransformer())])

    x = pipeline.fit_transform([t.text for t in labeled_tweets]).toarray()
    y = np.array([t.label for t in labeled_tweets])

    classifiers = [
        KNeighborsClassifier(3),
        SVC(gamma=2, C=1),
        DecisionTreeClassifier(max_depth=5),
        MultinomialNB(),
        LogisticRegression()
    ]
    # FIXME: Write sLDA wrapper that extends ClassifierI for inclusion above

    cv = cross_validation.KFold(len(y), opts.k_folds, shuffle=True, random_state=1234)
    metric_names = metric_names()
    print '\t'.join(['model' + ' ' * 8] + metric_names)
    for clf in classifiers:
        results = []
        for train, test in cv:
            truth = y[test]
            pred = clf.fit(x[train], y[train]).predict(x[test])
            results.append(score(truth, pred))
        results_avg = summarize(results, opts.k_folds)
        print str(clf)[:13] + '\t' + '\t'.join([('%.2f' % results_avg[m]) for m in metric_names])
