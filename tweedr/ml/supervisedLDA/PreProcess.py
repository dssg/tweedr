#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import types
import string
from pattern.en.wordlist import BASIC

stopwords = \
    '''texas,oklahoma,im,rt,irene,sandy,a,able,about,across,after,all,almost,also,am,among,an,and,any,are,as,at,be,because,been,but,by,can,cannot,could,dear,did,do,does,either,else,ever,every,for,from,get,got,had,has,have,he,her,hers,him,his,how,however,i,if,in,into,is,it,its,just,least,let,like,likely,may,me,might,most,must,my,neither,no,nor,not,of,off,often,on,only,or,other,our,own,rather,said,say,says,she,should,since,so,some,than,that,the,their,them,then,there,these,they,this,tis,to,too,twas,us,wants,was,we,were,what,when,where,which,while,who,whom,why,will,with,would,yet,you,your'''
stopwords = stopwords.split(',')
stopwords.extend(BASIC)


def processTweet(tweet):
    if isinstance(tweet, types.NoneType):
        return ' '
    tweet = tweet.lower()
    tweet = re.sub('((www\.[/s]+)|(https?://[^\s]+))', ' ', tweet)
    tweet = tweet.translate(None, string.punctuation)
    tweet = re.sub("@[^\s]+", ' ', tweet)
    tweet = re.sub('[\s]+', ' ', tweet)
    tweet = re.sub(r"#([^\s]+)", r'\1', tweet)
    tweet = tweet.strip('\'"')
    words = tweet.split()
    words = [word for word in words if not word in stopwords]
    words = ' '.join(words)
    words = words.strip()
    return words


def is_ascii(tweet):
    for c in tweet:
        if ord(c) >= 128:
            return False
    return True
