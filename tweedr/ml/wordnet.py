#!/usr/bin/python
# -*- coding: utf-8 -*-

from pattern.en import wordnet
from pattern.vector import stem


def WordnetFeatures(token):
    synset = wordnet.synsets(token)
    if len(synset) > 0:
        synset = synset[0]
        hypernym = synset.hypernyms(depth=2, recursive=True)
#       hypernym.extend(synset.hyponyms(depth=2,recursive=True))
        return [hyper.senses[0] for hyper in hypernym]
    else:
        return []


def WordNet(document):
    return [WordnetFeatures(token) for token in document]


def token_hypernyms(token, recursive, depth):
    '''Stem each token using default stemmer from the pattern library (PORTER?)'''
    for synset in wordnet.synsets(stem(token)):
        for hypernym in synset.hypernyms(recursive, depth):
            for sense in hypernym.senses:
                yield sense


def hypernyms(document, recursive=True, depth=1):
    '''Iterate through all senses for all 1-away hypernyms. E.g.:

        print map(list, hypernyms(document))
    '''
    for token in document:
        yield token_hypernyms(token, recursive, depth)
