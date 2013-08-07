#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import string


def processTweet(tweet):
    tweet = tweet.lower()
    tweet = re.sub('((www\.[/s]+)|(https?://[^\s]+))', ' ', tweet)
    tweet = re.sub("@[^\s]+", ' ', tweet)
    tweet = re.sub('[\s]+', ' ', tweet)
    tweet = re.sub(r"#([^\s]+)", r'\1', tweet)
    tweet = tweet.strip('\'"')
    return tweet


def is_ascii(tweet):
    for c in tweet:
        if ord(c) >= 128:
            return False
    return True
