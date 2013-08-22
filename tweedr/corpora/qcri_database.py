#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
from sets import Set

from tweedr.models import DBSession, DamageClassification


class DamageClassifiedCorpus(object):

    def __init__(self):
        labeled_tweets = \
            np.array(DBSession.query(DamageClassification).filter(DamageClassification.mturk_code
                == 'QCRI').limit(1000).all())
        labeled_tweets = map(lambda x: (x.text, int(x.label)), labeled_tweets)
        self.dataset = labeled_tweets

    def __iter__(self):
        return iter(self.dataset)



test_set = DamageClassifiedCorpus()
