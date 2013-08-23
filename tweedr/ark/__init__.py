import sys

import logging
logger = logging.getLogger(__name__)


def main():
    '''Example usage:

    echo "The Fulton County Grand Jury said Friday an investigation of Atlanta's recent primary election produced no evidence that any irregularities took place." | python -m tweedr.ark.__init__
    '''
    if sys.stdin.isatty():
        logger.error('You must pipe in a string')
        exit(1)

    from tweedr.ark.java import TwitterNLP
    tagger = TwitterNLP()

    for line in sys.stdin:
        print '[input]', line.strip()
        tag_line = tagger.predict(line)
        print '[output]', tag_line

if __name__ == '__main__':
    main()
