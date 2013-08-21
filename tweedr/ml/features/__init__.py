# each feature function takes an N-long document (list of strings) and returns an N-long list
#   of lists/tuples of features (i.e., strings) to add to the total data for that sentence.
#   often the list will contain lists that are 1-long
from itertools import izip, chain


def spacer(xs):
    return [' '.join(xs)]


def featurize_adjacent(tokens, feature_functions):
    feature_functions_results = [feature_function(tokens) for feature_function in feature_functions]
    list_of_token_features = []
    #add token features
    for token_featuress in izip(*feature_functions_results):
        list_of_token_features.append(list(chain.from_iterable(token_featuress)))
    #add features to the left and to the right
    i = 0
    while i < len(list_of_token_features):
        j = list_of_token_features[i]
        it = [k for k in j]
        if i > 0:
            a = list_of_token_features[i - 1]
            c = ['^^^' + k for k in a]
            try:
                c.pop(0)
            except IndexError:
                pass
            it += c

        if i < len(list_of_token_features) - 1:
            b = list_of_token_features[i + 1]
            d = ['$$$' + k for k in b]
            try:
                d.pop(0)
            except IndexError:
                pass
            it += d
        i = i + 1
        yield chain.from_iterable([it])


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
    from tweedr.ml.features.sets import all_feature_functions
    for line in sys.stdin:
        # tokenize the document on whitespace
        tokens = token_re.findall(line)
        # apply all feature functions
        tokens_features = featurize(tokens, all_feature_functions)
        for i, token_features in enumerate(tokens_features):
            print i, list(token_features)

if __name__ == '__main__':
    main()
