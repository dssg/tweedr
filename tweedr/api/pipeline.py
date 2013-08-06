import sys
import json
import pybloomfilter
import logging
import tempfile

logger = logging.getLogger(__name__)


class StringProtocol(object):
    pass


class DictProtocol(object):
    pass


class TweetDictProtocol(DictProtocol):
    '''This merely asserts that the following fields will exist and have reasonable values:

        text: String
        id: String
        author: String
    '''


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
    INPUT = DictProtocol
    OUTPUT = TweetDictProtocol

    whitespace = {ord('\t'): u' ', ord('\n'): u' ', ord('\r'): u''}

    def __call__(self, dict_):
        # ensure text. different sources call it different things.
        if 'text' in dict_:
            dict_['text'] = dict_['text'].translate(self.whitespace)
        elif 'body' in dict_:
            dict_['text'] = dict_.pop('body').translate(self.whitespace)
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


class TextCounter(Mapper):
    INPUT = TweetDictProtocol
    OUTPUT = TweetDictProtocol

    def __init__(self):
        # Use an in-memory bloomfilter for now, maybe move to pyreBloom if we need something threadsafe?
        bloomfilter_filepath = tempfile.NamedTemporaryFile(delete=False).name
        logger.debug('Saving bloomfilter to %s', bloomfilter_filepath)
        # pybloomfilter.BloomFilter(capacity, error_rate, filename)
        self.bloomfilter = pybloomfilter.BloomFilter(10000000, 0.001, bloomfilter_filepath)
        self.seen = dict()

    def __call__(self, dict_):
        text = dict_['text']

        # bloomfilter.add(...) returns True if item is already in the filter
        if self.bloomfilter.add(text):
            # we only start to store counts when we see an item more than once
            self.seen[text] = dict_['count'] = self.seen.get(text, 1) + 1
        else:
            dict_['count'] = 1

        return dict_


class LineStream(Mapper):
    INPUT = DictProtocol
    OUTPUT = None

    def __init__(self, stream):
        self.stream = sys.stdout

    def __call__(self, dict_):
        json.dump(dict_, self.stream)
        self.stream.write('\n')
        # flush might be unnecessary in production
        self.stream.flush()


class Pipeline(object):
    def __init__(self, *mappers):
        logger.info('%s -> [pipeline] -> %s', mappers[0].INPUT, mappers[-1].OUTPUT)
        # type-check the connections between the provided mappers
        total_errors = 0
        for from_pipe, to_pipe in zip(mappers, mappers[1:]):
            # Python lets you use `a <= b` to say `a is a subclass of b`
            # SuperClass >= Class is true
            # Class >= Class is true
            # Class >= SuperClass is false
            if from_pipe.OUTPUT < to_pipe.INPUT:
                logger.error('Pipeline cannot connect mappers: %s[%s] -> %s[%s]',
                    from_pipe.__class__.__name__, from_pipe.OUTPUT.__name__,
                    to_pipe.__class__.__name__, to_pipe.INPUT.__name__)
                total_errors += 1
        if total_errors > 0:
            raise TypeError('Pipeline types do not match!')
        self.mappers = mappers

    def __call__(self, payload):
        logger.notset('Pipeline processing payload: %s', payload)
        # TODO: maybe wrap with a try-except here?
        for mapper in self.mappers:
            payload = mapper(payload)
            if payload is None:
                break
        return payload


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Run tweets from STDIN through the tweedr pipeline, output to STDOUT.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Log extra output')
    # parser.add_argument('--files', nargs='*')
    opts = parser.parse_args()

    # bump threshold down to show info=20, debug=10, and silly=5 if --verbose is set
    if opts.verbose:
        logger.setLevel('SILLY')

    if sys.stdin.isatty():
        raise IOError('You must provide input via STDIN')

    pipeline = Pipeline(
        EmptyLineFilter(),
        JSONParser(),
        IgnoreMetadata(),
        TweetStandardizer(),
        TextCounter(),
        LineStream(sys.stdout),
    )

    logger.debug('Pipeline created')

    for i, line in enumerate(sys.stdin):
        pipeline(line)

    logger.info('Processed %d lines', i)
    logger.debug('Pipeline exited')


if __name__ == '__main__':
    main()
