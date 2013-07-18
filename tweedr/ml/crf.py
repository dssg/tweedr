# Trainer and Tagger come pretty much directly from
#   git://github.com/chbrown/nlp.git/python/det/crf.py, which is MIT Licensed
import crfsuite
import logging

logger = logging.getLogger(__name__)


class Trainer(crfsuite.Trainer):
    """
    Inherit crfsuite.Trainer to implement message() function, which receives
    progress messages from a training process.
    """
    def message(self, s):
        logger.debug('Trainer.message: %s', s)

    def append_raw(self, features_seq, labels):
        # len(labels) = len(features_seq) = length of sentence / sequence
        # labels is a tuple of strings, features_seq is an tuple/list of variable-length lists of strings.
        # this just wraps all the data / labels with crfsuite types
        items = crfsuite.ItemSequence()
        for features in features_seq:
            item = crfsuite.Item()
            for feature in features:
                if isinstance(feature, tuple):
                    attribute = crfsuite.Attribute(*feature)
                else:
                    attribute = crfsuite.Attribute(feature)
                item.append(attribute)
            items.append(item)

        # labels = crfsuite.StringList(labels)
        self.append(items, tuple(labels), 0)

    def save(self, model_path):
        # Use L2-regularized SGD and 1st-order dyad features.
        self.select('l2sgd', 'crf1d')

        # This demonstrates how to list parameters and obtain their values.

        # Set the coefficient for L2 regularization to 0.1
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

    def tag(self, data):
        # Obtain the label sequence predicted by the tagger.
        self.set(data)
        return self.viterbi()

    def tag_raw(self, data):
        # data is a list of lists, which may very well be just 1-long
        # data = [['The'], ['man'], ['barked']]
        # The sublists maybe contain tuples (of string->float pairs)
        # data = [['The', ('first', 1)], ['man', 'human', ('first', 0)], ...]
        items = crfsuite.ItemSequence()
        for datum in data:
            item = crfsuite.Item()
            for feature in datum:
                if isinstance(feature, tuple):
                    item.append(crfsuite.Attribute(*feature))
                else:
                    item.append(crfsuite.Attribute(feature))
            items.append(item)

        return self.tag(items)
