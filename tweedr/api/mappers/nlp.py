from tweedr.api.mappers import Mapper
from tweedr.api.protocols import TweetDictProtocol
from tweedr.lib.text import token_re
from tweedr.ml.ark import TwitterNLP
from tweedr.ml.crf.classifier import CRF
from tweedr.ml.features import crf_feature_functions, featurize


import logging
logger = logging.getLogger(__name__)


class POSTagger(Mapper):
    INPUT = TweetDictProtocol
    OUTPUT = TweetDictProtocol

    def __init__(self):
        self.tagger = TwitterNLP()

    def __call__(self, tweet):
        '''Enhances the input tweet with POS tags, using only the tweet["text"] value:

            {
                ...
                "tokens": "@Donnie I hear ya and I hate earthquakes in Cali too ! But I still love living in LA ! :)",
                "pos": "@ O V O & O V N P ^ R , & O R V V P ^ ,",
                ...
            }

        The `tokens` and `pos` values can be split on whitespace to get equal-length lists of strings.
        '''
        tokens, pos_tags = self.tagger.tokenize_and_tag(tweet['text'])
        tweet['tokens'] = tokens
        tweet['pos'] = pos_tags
        return tweet


class SequenceTagger(Mapper):
    INPUT = TweetDictProtocol
    OUTPUT = TweetDictProtocol

    def __init__(self):
        self.crf = CRF.default()
        logger.info('SequenceTagger initialized')

    def __call__(self, tweet):
        text = tweet['text'].encode('utf8')
        tokens = token_re.findall(text)

        # tokens_features = map(list, featurize(tokens, crf_feature_functions))
        tokens_features = featurize(tokens, crf_feature_functions)
        labels = self.crf.predict([tokens_features])[0]
        tweet['labels'] = labels

        return tweet
