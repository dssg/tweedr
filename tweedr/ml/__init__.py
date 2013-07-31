from sklearn import base, metrics
from tweedr.lib import Counts


class ClassifierI(base.ClassifierMixin):
    '''
    I realize using this isn't Pythonic, but it's a way to remind myself what
    method sklearn-type classifiers are expected to implement.

    * `X`: an iterable of data points, each of which might be a point in many-dimensional space, a list of strings, etc.
    * `y`: an iterable of discrete labels, each of which may be a string, or a True/False value, or just an integer (not a float).
    '''
    def __init__(self, *args, **kw):
        pass

    # def decision_function(self, X):
    #     '''Predict confidence scores for samples.'''
    #     raise NotImplementedError(__doc__)

    def fit(X, y):
        '''Fit the model according to the given training data.'''
        raise NotImplementedError(__doc__)

    def fit_transform(X, y=None):
        '''Fit to data, then transform it'''
        raise NotImplementedError(__doc__)

    def get_params(deep=False):
        '''Get parameters for the estimator'''
        raise NotImplementedError(__doc__)

    def predict(X):
        '''Predict class labels for samples in X.'''
        raise NotImplementedError(__doc__)

    # def score(X, y):
    #     '''Returns the mean accuracy on the given test data and labels.'''
    #     raise NotImplementedError(__doc__)

    def set_params(**params):
        '''Set the parameters of the estimator.'''
        raise NotImplementedError(__doc__)

    def transform(X, threshold=None):
        '''Reduce X to its most important features.'''
        raise NotImplementedError(__doc__)


def print_metrics_summary(gold_labels, predicted_labels, sample=0):
    print '''    Accuracy: {accuracy}
    P/R: {precision:.4f}/{recall:.4f}
    F1: {fscore:.4f}'''.format(
        accuracy=metrics.accuracy_score(gold_labels, predicted_labels),
        precision=metrics.precision_score(gold_labels, predicted_labels),
        recall=metrics.recall_score(gold_labels, predicted_labels),
        fscore=metrics.f1_score(gold_labels, predicted_labels)
    )

    if sample > 0:
        print 'Sample of classifications '
        for _, gold, predicted in zip(xrange(sample), gold_labels, predicted_labels):
            print '  gold: {gold}, predicted: {predicted}'.format(gold=gold, predicted=predicted)


def compare_labels(gold_labels, predicted_labels, null_label):
    counts = Counts()
    for gold_label, predicted_label in zip(gold_labels, predicted_labels):
        counts.comparisons += 1
        if gold_label != null_label:
            if predicted_label == gold_label:
                counts.true_positives += 1
            else:
                counts.false_negatives += 1

        if gold_label == null_label:
            if predicted_label == gold_label:
                counts.true_negatives += 1
            else:
                counts.false_positives += 1

    return counts
