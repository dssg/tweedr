import sys

from tweedr.api import mappers
from tweedr.api.mappers import similar, nlp


import logging
logger = logging.getLogger(__name__)


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
        mappers.EmptyLineFilter(),
        mappers.JSONParser(),
        mappers.IgnoreMetadata(),
        mappers.TweetStandardizer(),
        similar.TextCounter(),
        similar.FuzzyTextCounter(),
        nlp.POSTagger(),
        mappers.LineStream(sys.stdout),
    )

    logger.debug('Pipeline created')

    try:
        for i, line in enumerate(sys.stdin):
            pipeline(line)
    except KeyboardInterrupt:
        logger.error('SIGINT received; Exiting.')

    logger.info('Processed %d lines', i)
    logger.debug('Pipeline exited')


if __name__ == '__main__':
    main()
