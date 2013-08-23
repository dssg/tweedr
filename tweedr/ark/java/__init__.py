import os
from subprocess import Popen, PIPE

import tweedr
from tweedr.ml.classifier import ClassifierI
from tweedr.lib.text import whitespace_unicode_translations

import logging
logger = logging.getLogger(__name__)

jar_path = os.path.join(tweedr.root, 'ext', 'ark-tweet-nlp-0.3.2.jar')


class TwitterNLP(ClassifierI):
    def __init__(self, *args, **kw):
        self.proc = Popen(['java', '-cp', jar_path, 'cmu.arktweetnlp.RunTagger',
            '--input-format', 'text', '--output-format', 'pretsv'],
            stdin=PIPE, stdout=PIPE, stderr=PIPE)

        logger.info('cmu.arktweetnlp.RunTagger Java VM initialized with PID: %d', self.proc.pid)

    def fit(self, X, y):
        raise NotImplementedError('TwitterNLP is pre-trained; re-training is not supported.')

    def predict(self, X):
        # return only the labels (the POS tags)
        return self.parse_string(X)[1]

    # additional fields below are not required by ClassifierI, except that
    # they are called in predict
    def tokenize_and_tag(self, document):
        # only return the first two lines (tokens and labels)
        return self.parse_string(document)[:2]

    def parse_string(self, document):
        '''
        Take a single string, remove any CR / LF / tab whitespace, and run it
        through TwitterNLP as an individual sequence of text.

            `document` String line of input

        Returns a tuple of strings, each of which is an equal-length (after
        `split`'ing) whitespace-separated sequence of tokens / POS tags /
        confidences.
        '''
        # sanitize the input and convert to bytestring
        if not isinstance(document, unicode):
            document = document.decode('utf8')
        string = document.translate(whitespace_unicode_translations).encode('utf8').strip()

        # write input with EOL marker (RunTagger won't return tags until it hits a newline)
        self.proc.stdin.write(string)
        self.proc.stdin.write('\n')

        # wait for output
        result = self.proc.stdout.readline()
        # no available stdout (the empty string) means there was an error
        if result == '':
            for stderr_line in self.proc.stderr:
                logger.error(stderr_line.rstrip())
            raise IOError('cmu.arktweetnlp.RunTagger error')

        # output of cmu.arktweetnlp.RunTagger is TOKENS<tab>TAGS<tab>CONFIDENCES<tab>ORIGINAL
        parts = result.split('\t')
        # cut off the original input, which is parts[3]
        return parts[0:3]
