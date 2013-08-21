from tweedr.ml import wordnet, lexicon_list


def is_transportation(document):
    return [['TRANSPORTATION'] if token in lexicon_list.transportation else [] for token in document]


def is_building(document):
    return [['BUILDING'] if token in lexicon_list.buildings else [] for token in document]


def hypernyms(document, recursive=True, depth=1):
    '''Iterate through all senses for all 1-away hypernyms. E.g.:

        print map(list, hypernyms(document))
    '''
    for token in document:
        yield wordnet.token_hypernyms(token, recursive, depth)
