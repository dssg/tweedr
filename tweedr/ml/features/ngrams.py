from tweedr.ml.features import spacer


def unigrams(document):
    return [[token] for token in document]


def rbigrams(document):
    grams = zip(document, document[1:] + ['$$$'])
    return map(spacer, grams)


def lbigrams(document):
    grams = zip(['^^^'] + document[:-1], document)
    return map(spacer, grams)


def ctrigrams(document):
    grams = zip(['^^^'] + document[:-1], document, document[1:] + ['$$$'])
    return map(spacer, grams)


def unique(document):
    # TODO: unique doesn't really belong here, but doesn't quite merit its own module
    seen = {}
    features = []
    for token in document:
        features.append(['UNIQUE'] if token not in seen else [])
        seen[token] = 1
    return features
