from sklearn import metrics
from tweedr.lib import Counts


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
    # produces a Counts object with values:
    #  .true_positives
    #  .false_negatives
    #  .true_negatives
    #  .false_positives
    #  .comparisons = SUM of the others
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
