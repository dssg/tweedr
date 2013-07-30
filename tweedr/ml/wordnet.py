#!/usr/bin/python
# -*- coding: utf-8 -*-

from pattern.en import wordnet


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
