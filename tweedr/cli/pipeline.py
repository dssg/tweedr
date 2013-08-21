import argparse
import sys
from tweedr.api import pipeline
from tweedr.api.mappers import basic, similar, nlp

import logging
logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Run tweets from STDIN through the tweedr pipeline, output to STDOUT.')
    parser.add_argument('-v', '--verbose', action='store_true', help='Log extra output')
    opts = parser.parse_args()

    # bump threshold down to show info=20, debug=10, and silly=5 if --verbose is set
    if opts.verbose:
        logger.setLevel('SILLY')

    if sys.stdin.isatty():
        raise IOError('You must provide input via STDIN')

    cli_pipeline = pipeline.Pipeline(
        basic.EmptyLineFilter(),
        basic.JSONParser(),
        basic.IgnoreMetadata(),
        basic.TweetStandardizer(),
        similar.TextCounter(),
        similar.FuzzyTextCounter(),
        nlp.POSTagger(),
        nlp.SequenceTagger(),
        nlp.DBpediaSpotter(),
        basic.LineStream(sys.stdout),
    )

    logger.debug('Pipeline created')

    try:
        for i, line in enumerate(sys.stdin):
            cli_pipeline(line)
    except KeyboardInterrupt:
        logger.critical('SIGINT received; Exiting.')

    logger.info('Processed %d lines', i)
    logger.debug('Pipeline exited')


if __name__ == '__main__':
    main()
