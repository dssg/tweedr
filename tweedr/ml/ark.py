import os
import sys
from subprocess import Popen, PIPE

import tweedr
from tweedr.lib.text import whitespace_unicode_translations

import logging
logger = logging.getLogger(__name__)

# start a long-running process when this module is imported
jar_path = os.path.join(tweedr.root, 'ext', 'ark-tweet-nlp-0.3.2.jar')
tagger_proc = Popen(['java', '-cp', jar_path, 'cmu.arktweetnlp.RunTagger',
    '--input-format', 'text', '--output-format', 'pretsv'],
    stdin=PIPE, stdout=PIPE, stderr=PIPE)

logger.info('cmu.arktweetnlp.RunTagger Java VM initialized with PID: %d', tagger_proc.pid)


def communicate_bytewise(raw, timeout_seconds):
    '''Maybe completely unnecessary due to stdout.readline()'''
    from tweedr.lib.readers import read_until
    from tweedr.lib.timeout import timeout_after, TimeoutError

    import fcntl
    # fcntl.fcntl(tagger_proc.stdout.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)
    fcntl.fcntl(tagger_proc.stderr.fileno(), fcntl.F_SETFL, os.O_NONBLOCK)

    @timeout_after(timeout_seconds)
    def buffering_loop():
        return read_until(tagger_proc.stdout, '\n')

    try:
        return buffering_loop()
    except TimeoutError:
        logger.error('Timed out, reading from STDERR...')
        stderr_string = read_until(tagger_proc.stderr, ('', '\n'))
        logger.critical(stderr_string)
        raise


def tag(string):
    '''
    run_tagger takes a single string, removes any CR / LF / tab whitespace, and runs
    it through TwitterNLP as an individual sequence of text.

    Returns list of tab-separated lines (without newlines).
    '''
    # sanitize the input and convert to bytestring
    if not isinstance(string, unicode):
        string = string.decode('utf8')
    string = string.translate(whitespace_unicode_translations).encode('utf8').strip()

    # write input with EOL marker (RunTagger won't return tags until it hits a newline)
    tagger_proc.stdin.write(string)
    tagger_proc.stdin.write('\n')

    # wait for output
    result = tagger_proc.stdout.readline()
    # no available stdout (the empty string) means there was an error
    if result == '':
        for stderr_line in tagger_proc.stderr:
            logger.error(stderr_line.rstrip())
        raise IOError('cmu.arktweetnlp.RunTagger error')

    # output of cmu.arktweetnlp.RunTagger is TOKENS<tab>TAGS<tab>CONFIDENCES<tab>ORIGINAL
    parts = result.split('\t')
    # cut off the original input, which is parts[3]
    return parts[0:3]


def main():
    if sys.stdin.isatty():
        logger.error('You must pipe in a string')
        exit(1)

    for line in sys.stdin:
        print '[input]', line
        tokens, tags, confidences = tag(line)
        print '[tokens]', tokens
        print '[tags]', tags
        print '[confidences]', confidences

if __name__ == '__main__':
    main()
