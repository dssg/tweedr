# the tagger is global, powered by the singleton module in tweedr.ml.ark
from tweedr.ark.java.singleton import tagger

import logging
logger = logging.getLogger(__name__)


def pos_tags(document):
    text = ' '.join(document)
    tokens_line, tags_line = tagger.tokenize_and_tag(text)
    tokens = tokens_line.split()
    tags = tags_line.split()

    if not (len(document) == len(tokens) == len(tags)):
        # TODO: make this warning unnecessary
        logger.critical('TwitterNLP tagger did not tokenize correctly: %s vs %s', text, tokens_line)
    return [[tag] for tag in tags]
