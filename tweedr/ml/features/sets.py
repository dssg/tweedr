from tweedr.ml.features import characters, dbpedia, lexicons, ngrams

crf_feature_functions = [
    ngrams.unigrams,
    characters.plural,
    lexicons.is_transportation,
    lexicons.is_building,
    characters.capitalized,
    characters.numeric,
    ngrams.unique,
    lexicons.hypernyms,
    dbpedia.features,
]

all_feature_functions = crf_feature_functions + [
    ngrams.rbigrams,
    ngrams.lbigrams,
    ngrams.ctrigrams,
]

classifier_feature_functions = [
    ngrams.unigrams,
]
