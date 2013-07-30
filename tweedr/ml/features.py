# each feature function takes an N-long document (list of strings) and returns an N-long list
#   of lists/tuples of features (i.e., strings) to add to the total data for that sentence.
#   often the list will contain lists that are 1-long
from lexicon_list import transportation, buildings


def spacer(xs):
    return [' '.join(xs)]


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


def plural(document):
    return [['PLURAL'] if token.endswith('s') else [] for token in document]


def is_transportation(document):
    return [['TRANSPORTATION'] if token in transportation else [] for token in document]


def is_building(document):
    return [['BUILDING'] if token in buildings else [] for token in document]


def capitalized(document):
    return [['CAPITALIZED'] if token[0].isupper() else [] for token in document]


def numeric(document):
    return [['NUMERIC'] if token.isdigit() else [] for token in document]


def unique(document):
    seen = {}
    features = []
    for token in document:
        features.append(['UNIQUE'] if token not in seen else [])
        seen[token] = 1
    return features


all_feature_functions = [
    unigrams,
    rbigrams,
    lbigrams,
    ctrigrams,
    plural,
    capitalized,
    numeric,
    unique,
]


def featurize(tokens, feature_functions):
    '''Take a N-long list of strings (natural text), apply each feature function,
    and then unzip (transpose) and flatten so that we get a N-long list of
    arbitrarily-long lists of strings.
    '''
    # feature_sets = []
    # for feature_function in feature_functions:
    #     feature_set = feature_function(document)
    #     feature_sets.append(feature_set)
    # tokens_feature_sets = zip(*feature_sets)
    # tokens_features = map(flatten, tokens_feature_sets)

    # or replace the previous six lines with:
    features_groups = [feature_function(tokens) for feature_function in feature_functions]
    return [sum(tokens_features_group, []) for tokens_features_group in zip(*features_groups)]


def main():
    # example usage:
    # echo "The Fulton County Grand Jury said Friday an investigation of Atlanta's recent primary election produced no evidence that any irregularities took place." | python features.py
    import sys
    from tweedr.lib.text import token_re
    for line in sys.stdin:
        # tokenize the document on whitespace
        tokens = token_re.findall(line)
        # apply all feature functions
        tokens_features = featurize(tokens, all_feature_functions)
        for i, token_features in enumerate(tokens_features):
            print i, token_features

if __name__ == '__main__':
    main()
