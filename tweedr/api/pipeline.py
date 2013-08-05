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
    # @classmethod
    # def from_json(json_str):
    #     return json.loads(json_str)


class Mapper(object):
    '''Passthrough / interface'''
    INPUT = DictProtocol
    OUTPUT = DictProtocol

    def __call__(self, dict_):
        return dict_


class EmptyLineFilter(Mapper):
    INPUT = StringProtocol  # default
    OUTPUT = StringProtocol  # default

    def __call__(self, line):
        # ignore empty lines
        stripped_line = line.strip()
        if stripped_line:
            return stripped_line


class JSONParser(Mapper):
    INPUT = StringProtocol  # default
    OUTPUT = DictProtocol  # default

    def __call__(self, line):
        try:
            return json.loads(line)
        except ValueError:
            logger.critical('Could not parse JSON: %s', line)
            raise


class IgnoreMetadata(Mapper):
    # INPUT = DictProtocol  # default
    # OUTPUT = DictProtocol  # default
    def __call__(self, dict_):
        if 'info' not in dict_:
            return dict_


class AddCount(Mapper):
    # INPUT = DictProtocol  # default
    # OUTPUT = DictProtocol  # default
    def __init__(self):
        # Use an in-memory bloomfilter for now, maybe move to pyreBloom if we need something threadsafe?
        bloomfilter_filepath = tempfile.NamedTemporaryFile(delete=False).name
        logger.debug('Saving bloomfilter to %s', bloomfilter_filepath)
        # pybloomfilter.BloomFilter(capacity, error_rate, filename)
        self.bloomfilter = pybloomfilter.BloomFilter(10000000, 0.001, bloomfilter_filepath)
        self.seen = dict()

    def __call__(self, dict_):

        # ignore metadata entries

        # get main text. different sources call it different things
        try:
            text = dict_.get('body') or dict_['text']
        except KeyError:
            logger.critical('Could not find contentful entry in line: %s', dict_)
            raise

        # 1. classify
        # 1a. useful? not-useful?

        # 1b. infrastructure? other?
        # etc.

        # 2. cluster
        # .add(...) returns True if item is already in the filter
        if self.bloomfilter.add(text):
            # we only start to store counts when we see an item more than once
            self.seen[text] = dict_['count'] = self.seen.get(text, 1) + 1
        else:
            dict_['count'] = 1

        return dict_


class LineStream(Mapper):
    INPUT = DictProtocol  # default
    OUTPUT = None

    def __init__(self, stream):
        self.stream = sys.stdout

    def __call__(self, dict_):
        json.dump(dict_, self.stream)
        self.stream.write('\n')
        # flush might be unnecessary in production
        self.stream.flush()


class Pipeline(object):
    def __init__(self, *pipes):
        logger.info('%s -> [pipeline] -> %s', pipes[0].INPUT, pipes[-1].OUTPUT)
        # type-check the connections between the provided pipes
        total_errors = 0
        for pipe_out, pipe_in in zip(pipes, pipes[1:]):
            if pipe_out.OUTPUT != pipe_in.INPUT:
                logger.error('Pipeline cannot connect pipes: %s[%s] -> %s[%s]',
                    pipe_out.__class__.__name__, pipe_out.OUTPUT.__name__,
                    pipe_in.__class__.__name__, pipe_in.INPUT.__name__)
                total_errors += 1
        if total_errors > 0:
            raise TypeError('Pipeline types do not match!')
        self.pipes = pipes

    def __call__(self, payload):
        logger.notset('Pipeline processing payload: %s', payload)
        # TODO: maybe wrap with a try-except here?
        for pipe in self.pipes:
            payload = pipe(payload)
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
        AddCount(),
        LineStream(sys.stdout),
    )

    logger.debug('Pipeline created')

    for i, line in enumerate(sys.stdin):
        pipeline(line)

    logger.info('Processed %d lines', i)
    logger.debug('Pipeline exited')


if __name__ == '__main__':
    main()
