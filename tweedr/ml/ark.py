import os
import sys
from StringIO import StringIO
from subprocess import Popen, PIPE

import tweedr

jar_path = os.path.join(tweedr.root, 'ext', 'ark-tweet-nlp-0.3.2.jar')

# start a long-running process when this module is required
tagger_proc = Popen(['java', '-cp', jar_path, 'cmu.arktweetnlp.RunTagger',
    '--input-format', 'text', '--output-format', 'pretsv'],
    stdin=PIPE, stdout=PIPE, stderr=PIPE)
# -server will pre-compile more, but start up slower
# -XX:+TieredCompilation -- not sure what effect this has.

print >> sys.stderr, 'cmu.arktweetnlp.RunTagger initialized with PID:', tagger_proc.pid

# output of cmu.arktweetnlp.RunTagger is TOKENS<tab>TAGS<tab>CONFIDENCE<tab>ORIGINAL


def run_tagger(string):
    '''run_tagger expects to receive a single line of input, ended by a newline character.
    weird things will happen if you hand it multiple lines of input;
    the first line will be tagged and returned, but this will leave unread output
    in the subprocess, which will be prepended to any subsequent calls to this method.
    '''
    # maybe just remove all newlines from the string?
    tagger_proc.stdin.write(string)

    output_buffer = StringIO()
    while True:
        # we have to read in bytes one-by-one because we have to break as soon as we hit a newline
        byte = tagger_proc.stdout.read(1)
        output_buffer.write(byte)
        if byte == '\n':
            break

    output = output_buffer.getvalue()
    output_buffer.close()

    # Tokenization \t POSTags \t Confidences \t (original data...)
    parts = output.split('\t')
    # cut off the original, which is parts[3]
    return parts[0:3]


if __name__ == '__main__':
    for line in sys.stdin:
        tokens, tags, confidences = run_tagger(line)
        print 'tokens', tokens
        print 'tags', tags
        print 'confidences', confidences
