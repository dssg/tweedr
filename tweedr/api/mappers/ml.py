from sklearn import feature_extraction, pipeline
from tweedr.lib.text import token_re
from tweedr.ml.features import featurize, characters, lexicons, ngrams
from tweedr.api.mappers import Mapper
from tweedr.api.protocols import TweetDictProtocol

import logging
logger = logging.getLogger(__name__)


class CorpusClassifier(Mapper):
    INPUT = TweetDictProtocol
    OUTPUT = TweetDictProtocol

    feature_functions = [
        ngrams.unigrams,
        characters.plural,
        lexicons.is_transportation,
        lexicons.is_building,
        characters.capitalized,
        characters.numeric,
        ngrams.unique,
        lexicons.hypernyms,
    ]

    def tokenizer(self, text):
        tokens = token_re.findall(text)
        tokens_features = featurize(tokens, self.feature_functions)
        for token_features in tokens_features:
            for feature in token_features:
                yield feature

    def __init__(self, datasource, classifier):
        logger.info('Training %s on %s', classifier.__class__.__name__, datasource.__class__.__name__)

        # datasource yields (label, text) pairs
        y, X = zip(*datasource)

        self.name = datasource.__class__.__name__ + ':' + classifier.__class__.__name__
        self.pipeline = pipeline.Pipeline([
            ('dictionary', feature_extraction.text.CountVectorizer(tokenizer=self.tokenizer)),
            ('tfidf', feature_extraction.text.TfidfTransformer()),
            ('classifier', classifier),
        ])

        self.pipeline.fit(X, y)

    def __call__(self, tweet):
        text = tweet['text']
        y = self.pipeline.predict([text])[0]

        if 'classification' not in tweet:
            tweet['classification'] = []

        tweet['classification'].append({
            'name': self.name,
            'label': y,
        })

        return tweet
