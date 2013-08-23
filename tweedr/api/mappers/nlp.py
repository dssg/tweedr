import os
import itertools
import requests
from tweedr.api.mappers import Mapper
from tweedr.api.protocols import TweetDictProtocol
from tweedr.lib.text import token_re, zip_boundaries
from tweedr.ml.features import featurize, characters, dbpedia, lexicons, ngrams
from tweedr.ark.java import TwitterNLP
from tweedr.ml.crf.classifier import CRF

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

    feature_functions = [
        ngrams.unigrams,
        characters.plural,
        lexicons.is_transportation,
        lexicons.is_building,
        characters.capitalized,
        characters.numeric,
        ngrams.unique,
        lexicons.hypernyms,
        dbpedia.spotlight,
    ]

    def __init__(self):
        self.crf = CRF.default(self.feature_functions)
        logger.info('SequenceTagger initialized')

    def __call__(self, tweet):
        text = tweet['text']
        tokens = token_re.findall(text)

        # tokens_features = map(list, featurize(tokens, crf_feature_functions))
        tokens_features = featurize(tokens, self.feature_functions)

        null_label = 'None'
        labels = self.crf.predict([tokens_features])[0]
        # tweet['labels'] = labels

        if 'sequences' not in tweet:
            tweet['sequences'] = []

        for sequence_label, entries in itertools.groupby(zip_boundaries(labels), lambda tup: tup[0]):
            if sequence_label != null_label:
                labels, starts, ends = zip(*entries)

                tweet['sequences'].append({
                    'text': sequence_label,
                    'start': starts[0],
                    'end': ends[-1],
                })

        return tweet


class DBpediaSpotter(Mapper):
    INPUT = TweetDictProtocol
    OUTPUT = TweetDictProtocol

    def __init__(self, confidence=0.1, support=10):
        self.annotate_url = '%s/rest/annotate' % os.environ.get('SPOTLIGHT', 'http://spotlight.sztaki.hu:2222')
        self.confidence = confidence
        self.support = support
        logger.info('DBpediaSpotter initialized')

    def __call__(self, tweet):
        text = tweet['text']

        if 'dbpedia' not in tweet:
            tweet['dbpedia'] = []

        r = requests.post(self.annotate_url,
            headers=dict(Accept='application/json'),
            data=dict(text=text, confidence=self.confidence, support=self.support))
        Resources = r.json().get('Resources', [])

        for Resource in Resources:
            start = int(Resource['@offset'])
            surface_form = Resource['@surfaceForm']
            types = Resource['@types']

            dbpedia_resource = {
                'text': surface_form,
                'start': start,
                'end': start + len(surface_form),
                'uri': Resource['@URI'],
                'types': types.split(',') if types else [],
            }

            tweet['dbpedia'].append(dbpedia_resource)

        return tweet
