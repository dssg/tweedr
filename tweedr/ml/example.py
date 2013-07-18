import re
import sys
import argparse

from tweedr.lib import flatten, bifurcate
from tweedr.models import DBSession, TokenizedLabel, Label
from tweedr.ml import crf
from tweedr.ml.features import all_feature_functions

print >> sys.stderr, 'Tweet count started.'
print 'There are %d labels in the database.' % DBSession.query(Label).count()
print 'There are %d tokenized labels in the database.' % DBSession.query(TokenizedLabel).count()


def main(test_proportion, max_data, model_path):
    tokenized_labels = DBSession.query(TokenizedLabel).limit(max_data).all()

    test, train = bifurcate(tokenized_labels, test_proportion, shuffle=True)

    trainer = crf.Trainer()

    # e.g., tokenized_label =
    # <TokenizedLabel dssg_id=23346 token_start=13 token_end=16
    #    tweet=Tornado Kills 89 in Missouri. http://t.co/IEuBas5 token_type=i18 token= 89 id=5>
    for tokenized_label in train:
        label_start, label_end = (tokenized_label.token_start, tokenized_label.token_end)

        text = tokenized_label.tweet
        token_spans_tokens = [(m.span(), m.group(0)) for m in re.finditer('\S+', text)]
        # token_spans, tokens = zip(*token_spans_tokens)

        tokens = []
        labels = []
        for (token_start, token_end), token in token_spans_tokens:
            # encode unicode token (database output) as string
            tokens.append(token.encode('utf8'))
            # we want to determine if this particular token in the original tweet overlaps
            #   with any portion of the selected label (label_span)
            if label_start <= token_start <= label_end or label_start <= token_end <= label_end:
                labels.append(str(tokenized_label.token_type))
            else:
                labels.append('NA')

        # produce and then flatten all the features
        data = map(flatten, zip(*[feature_function(tokens) for feature_function in all_feature_functions]))
        trainer.append_raw(data, labels)

    trainer.save(model_path)

    print 'Trainer saved to ' + model_path

    tagger = crf.Tagger(model_path)
    for tokenized_label in test:
        print 'Tagging:', tokenized_label

        tokens = re.findall('\S+', tokenized_label.tweet.encode('utf8'))
        print tokens

        data = map(flatten, zip(*[feature_function(tokens) for feature_function in all_feature_functions]))
        predicted_labels = tagger.tag_raw(data)
        print 'Predicted:'
        print predicted_labels
        # tokens = [item[0].attr for item in data]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train CRFSuite on data from the QCRI MySQL database')
    parser.add_argument('--test-proportion', type=float, default=0.1, help='The proportion of the total data to train on')
    parser.add_argument('--max-data', type=int, default=1000, help='Maximum data points to train and test on')
    parser.add_argument('--model-path', default='crf.model')
    parser.add_argument('--crfsuite-version', action='store_true', help='Print the active crfsuite version')
    opts = parser.parse_args()

    if opts.crfsuite_version:
        import crfsuite
        print 'CRFSuite v%s' % crfsuite.version()
    else:
        main(opts.test_proportion, opts.max_data, opts.model_path)
