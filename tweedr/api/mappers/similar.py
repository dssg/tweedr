from tweedr.api.mappers import Mapper
from tweedr.api.protocols import TweetDictProtocol

import logging
logger = logging.getLogger(__name__)

# for the bloomfilter
import tempfile
import pybloomfilter

# for simhashing
from hashes.simhash import simhash


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


class FuzzyTextCounter(Mapper):
    INPUT = TweetDictProtocol
    OUTPUT = TweetDictProtocol

    def __init__(self, threshold=0.97):
        self.threshold = threshold
        logger.debug('Simhash counter initialized with threshold of %0.3f', threshold)

        # list of all simhash objects
        self.simhashes = []
        # store is a lookup from a simhash hex to the original's id
        self.votes = dict()

    def __call__(self, dict_):
        text = dict_['text']
        self_simhash = simhash(text)

        fuzzy_count = 0
        sum_other_votes = 0
        for other_simhash in self.simhashes:
            if self_simhash.similarity(other_simhash) > self.threshold:
                # increment the votes of the others
                other_votes = self.votes[other_simhash.hash] = self.votes.get(other_simhash.hash, 1) + 1
                fuzzy_count += 1
                sum_other_votes += other_votes

        # should self.votes be elevated based on fuzzy_count?
        self.votes[self_simhash.hash] = 0

        # we should probably normalize based on the number of total votes
        dict_['fuzzy_count'] = fuzzy_count
        dict_['fuzzy_votes'] = sum_other_votes

        # store simhash in global state now that we've finished processing
        self.simhashes.append(self_simhash)
        return dict_
