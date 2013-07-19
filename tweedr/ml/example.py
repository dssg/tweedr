import argparse
from colorama import Fore

from tweedr.lib import flatten, bifurcate, Counts
from tweedr.lib.text import gloss
from tweedr.models import DBSession, TokenizedLabel, Label
from tweedr.ml import crf
from tweedr.ml.features import all_feature_functions


def stringify(o):
    return unicode(o).encode('utf8')


def main(test_proportion, max_data, model_path):
    print '%d labels' % DBSession.query(Label).count()
    for label in DBSession.query(Label):
        print '  %s = %s' % (label.id, label.text)

    tokenized_labels = DBSession.query(TokenizedLabel).limit(max_data).all()
    test, train = bifurcate(tokenized_labels, test_proportion, shuffle=True)
    print 'Training on %d, testing on %d' % (len(train), len(test))

    trainer = crf.Trainer()

    # e.g., tokenized_label =
    # <TokenizedLabel dssg_id=23346 token_start=13 token_end=16
    #    tweet=Tornado Kills 89 in Missouri. http://t.co/IEuBas5 token_type=i18 token= 89 id=5>
    for tokenized_label in train:
        tokens = map(stringify, tokenized_label.tokens)
        labels = map(stringify, tokenized_label.labels)
        # produce all the features and then flatten them
        data = map(flatten, zip(*[feature_function(tokens) for feature_function in all_feature_functions]))

        trainer.append_raw(data, labels)

    trainer.save(model_path)

    print 'Trainer saved to ' + model_path

    totals = Counts()

    tagger = crf.Tagger(model_path)
    for tokenized_label in test:
        # print 'Tagging:', tokenized_label

        tokens = map(stringify, tokenized_label.tokens)
        gold_labels = map(stringify, tokenized_label.labels)
        data = map(flatten, zip(*[feature_function(tokens) for feature_function in all_feature_functions]))

        predicted_labels = list(tagger.tag_raw(data))
        alignments = zip(tokens, gold_labels, predicted_labels)
        print gloss(alignments,
            prefixes=(Fore.WHITE, Fore.YELLOW, Fore.BLUE),
            postfixes=(Fore.RESET, Fore.RESET, Fore.RESET))

        counts = Counts()
        for gold_label, predicted_label in zip(gold_labels, predicted_labels):
            counts.comparisons += 1
            if gold_label != 'None':
                if predicted_label == gold_label:
                    counts.true_positives += 1
                else:
                    counts.false_negatives += 1

            if gold_label == 'None':
                if predicted_label == gold_label:
                    counts.true_negatives += 1
                else:
                    counts.false_positives += 1

            # if gold_label != 'None' and predicted_label != 'None':
            #     # non_null_partial_matches:
            #     #   the number of items that anything but None for both gold and predicted
            #     counts.non_null_partial_matches += 1
            #     if gold_label == predicted_label:
            #         counts.non_null_exact_matches += 1
            # if gold_label == predicted_label:
            #     counts.exact_matches += 1

        totals.add(counts)

        print '-' * 80

    print totals

    print 'Precision: %0.4f' % (
        float(totals.true_positives) /
        (totals.true_positives + totals.false_positives))
    print 'Recall: %0.4f' % (
        float(totals.true_positives) /
        (totals.true_positives + totals.false_negatives))

    # TODO: list top tokens for each label type


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train CRFSuite on data from the QCRI MySQL database')
    parser.add_argument('--test-proportion', type=float, default=0.1, help='The proportion of the total data to train on')
    parser.add_argument('--max-data', type=int, default=1000, help='Maximum data points to train and test on')
    parser.add_argument('--model-path', default='/tmp/crfsuite-ml-example.model')
    parser.add_argument('--crfsuite-version', action='store_true', help='Print the active crfsuite version')
    opts = parser.parse_args()

    if opts.crfsuite_version:
        print 'CRFSuite v%s' % crf.version
    else:
        main(opts.test_proportion, opts.max_data, opts.model_path)
