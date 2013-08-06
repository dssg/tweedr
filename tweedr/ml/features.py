# each feature function takes an N-long document (list of strings) and returns an N-long list
#   of lists/tuples of features (i.e., strings) to add to the total data for that sentence.
#   often the list will contain lists that are 1-long
import lexicon_list
import spotlight
from tweedr.ml.wordnet import hypernyms
from itertools import izip, chain


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
    return [['TRANSPORTATION'] if token in lexicon_list.transportation else [] for token in document]


def is_building(document):
    return [['BUILDING'] if token in lexicon_list.buildings else [] for token in document]


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


def get_pos(offset, document):
    doc_joined = " ".join(document)
    beginning = doc_joined[:offset]
    length = len(beginning.split(" ")) - 1
    return length


def dbpedia_features(document):
    doc_length = len(document)
    #URL will be replaced with ec2 ami instance once that is setup
    joined_string = (" ").join(document)
    annotations = spotlight.annotate('http://spotlight.dbpedia.org/rest/annotate', joined_string, confidence=0.4, support=10)
    positions = [[] for x in xrange(doc_length)]
    for a in annotations:
        surfaceForm = a["surfaceForm"]
        offset = a["offset"]
        type = a["types"]
        all_types = type.split(",")
        dbpedia_type = all_types[0]
        pos = get_pos(offset, document)
        words = surfaceForm.split(" ")
        len_words = len(words)
        try:
            if (len_words > 1 and str(dbpedia_type) != ""):
                c = pos
                num = 0
                while c < pos + len_words:
                    db = str(dbpedia_type)
                    positions[c] = [db.upper()]
                    num = num + 1
                    c = c + 1
            else:
                db = str(dbpedia_type)
                positions[pos] = [db.upper()]
                #if has type but is empty string set to "thing"
                if db == "":
                    positions[pos] = ["DBpedia:Thing".upper()]
        except AttributeError:
            positions[pos] = []
    return positions

crf_feature_functions = [
    unigrams,
    plural,
    is_transportation,
    is_building,
    capitalized,
    numeric,
    unique,
    hypernyms,
]

all_feature_functions = crf_feature_functions + [
    rbigrams,
    lbigrams,
    ctrigrams,
]


def featurize(tokens, feature_functions):
    '''Take a N-long list of strings (natural text), apply each feature function,
    and then unzip (transpose) and flatten so that we get a N-long list of
    arbitrarily-long lists of strings.
    '''
    feature_functions_results = [feature_function(tokens) for feature_function in feature_functions]
    for token_featuress in izip(*feature_functions_results):
        yield chain.from_iterable(token_featuress)


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
