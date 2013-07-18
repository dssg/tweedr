from mrjob.job import MRJob
from mrjob.protocol import JSONValueProtocol
import json


class WordCount(MRJob):
    '''
    The default MRJob.INPUT_PROTOCOL is `RawValueProtocol`, but we are reading tweets,
    so we'll add a parser before we even get to the mapper.
    '''
    # incoming line needs to be parsed (I think), so we set a protocol to do so
    INPUT_PROTOCOL = JSONValueProtocol

    def mapper(self, key, line):
        '''The key to the first mapper in the step-pipeline is always None.'''

        # GNIP-style streams sometimes have metadata lines, but we can just ignore them
        if 'info' in line and line['info']['message'] == 'Replay Request Completed':
            return

        # GNIP-style tweets have the tweet text in {'body': '...'} instead of the standard {'text': '...'}
        if 'body' not in line:
            raise Exception('Missing body field in tweet:\n  ' + json.dumps(line))

        text = line['body']
        yield '~~~TOTAL~~~', 1
        for token in text.split():
            yield token.lower(), 1

    def combiner(self, key, value_iter):
        yield key, sum(value_iter)

    def reducer(self, key, value_iter):
        yield key, sum(value_iter)


if __name__ == '__main__':
    WordCount.run()
