from tweedr.ml.ark import tag
from tweedr.api.mappers import Mapper
from tweedr.api.protocols import TweetDictProtocol


class POSTagger(Mapper):
    INPUT = TweetDictProtocol
    OUTPUT = TweetDictProtocol

    def __call__(self, tweet):
        tokens, tags, confidences = tag(tweet['text'])
        tweet['pos'] = dict(tokens=tokens, tags=tags, confidences=confidences)
        return tweet
