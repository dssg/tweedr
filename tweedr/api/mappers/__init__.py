import os
import sys
import json
from tweedr.lib.text import whitespace_unicode_translations
from tweedr.api.protocols import StringProtocol, DictProtocol, TweetDictProtocol

import logging
logger = logging.getLogger(__name__)


class Mapper(object):
    '''Passthrough / interface'''
    INPUT = DictProtocol
    OUTPUT = DictProtocol

    def __call__(self, dict_):
        return dict_


class EmptyLineFilter(Mapper):
    INPUT = StringProtocol
    OUTPUT = StringProtocol

    def __call__(self, line):
        # ignore empty lines
        stripped_line = line.strip()
        if stripped_line:
            return stripped_line


class JSONParser(Mapper):
    INPUT = StringProtocol
    OUTPUT = DictProtocol

    def __call__(self, line):
        try:
            return json.loads(line)
        except ValueError:
            logger.critical('Could not parse JSON: %s', line)
            raise


class IgnoreMetadata(Mapper):
    INPUT = DictProtocol
    OUTPUT = DictProtocol

    def __call__(self, dict_):
        if 'info' not in dict_:
            return dict_


class TweetStandardizer(Mapper):
    '''Ensures that a given dict being mapped through the pipeline has basic
    fields that come with every tweet, coalescing them into predictable names.

    This is necessary because different sources of tweets (e.g., raw Twitter,
    GNIP) name this information a variety of different things.

    The fields are:

        * `text` Unicode The tweet's textual content
        * `author` Unicode The Twitter screen name of the tweet's author
        * `id_str` Unicode The tweet's identifying snowflake, as assigned by
            Twitter when originally posted.

    See `TweetDictProtocol`'s documentation for more details.
    '''
    INPUT = DictProtocol
    OUTPUT = TweetDictProtocol

    def __call__(self, dict_):
        # ensure text. different sources call it different things.
        if 'text' in dict_:
            dict_['text'] = dict_['text'].translate(whitespace_unicode_translations)
        elif 'body' in dict_:
            dict_['text'] = dict_.pop('body').translate(whitespace_unicode_translations)
        else:
            logger.critical('Could not find text field in %s', dict_)
            raise KeyError("'text' | 'body'")

        # ensure author
        if 'actor' in dict_:
            dict_['author'] = dict_['actor']['preferredUsername']
        elif 'user' in dict_:
            dict_['author'] = dict_['user']['screen_name']
        else:
            logger.critical('Could not find author field in %s', dict_)
            raise KeyError("'actor.preferredUsername' | 'user.screen_name'")

        # ensure id
        if 'id_str' in dict_:
            dict_['id'] = dict_['id_str']
        else:
            dict_['id'] = dict_['id'].split(':')[-1]

        return dict_


class LineStream(Mapper):
    INPUT = DictProtocol
    OUTPUT = None

    def __init__(self, stream):
        self.stream = sys.stdout

    def __call__(self, dict_):
        json.dump(dict_, self.stream)
        self.stream.write(os.linesep)
        # flush might be unnecessary in production
        self.stream.flush()
