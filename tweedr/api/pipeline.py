import sys
import json
import logging

logger = logging.getLogger(__name__)


class Pipeline():
    '''Pipeline is a class because it's stateful, but it responds to calls like a function, too.'''
    def __call__(self, line):
        '''
        line -- string of input, maybe with trailing newline

        return string of output, *without* trailing newline
        '''
        logger.notset('Pipeline processing line: %s', line)

        try:
            obj = json.loads(line)
        except ValueError:
            logger.critical('Could not parse JSON: %s', line)
            raise

        # 1. classify
        # 1a. useful? not-useful?

        # 1b. infrastructure? other?
        # etc.

        return json.dumps(obj)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Run tweets from STDIN through the tweedr pipeline, output to STDOUT.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Log extra output')
    # parser.add_argument('--files', nargs='*')
    opts = parser.parse_args()

    # bump threshold down to show info=20, debug=10, and silly=5 if --verbose is set
    if opts.verbose:
        logger.setLevel('SILLY')

    logger.debug('Pipeline loading')
    pipeline = Pipeline()

    if sys.stdin.isatty():
        raise IOError('You must provide input via STDIN')

    for i, line in enumerate(sys.stdin):
        # TODO: maybe wrap with a try-except here?

        # absorb empty lines
        stripped_line = line.strip()
        if stripped_line:
            output = pipeline(line)
            sys.stdout.write(output)
            sys.stdout.write('\n')
            # if opts.verbose:
                # sys.stdout.flush()

    logger.debug('Pipeline processed all input (%d lines)', i)


if __name__ == '__main__':
    main()
