#!/usr/bin/python
# -*- coding: utf-8 -*-

from nltk.corpus import stopwords
from sets import Set
from gensim import corpora
from collections import Counter


# Writes a list to a particular file

def writeListToFile(mylist, filename):
    out_file = open(filename, 'w+')
    for item in mylist:
        out_file.write('%s\n' % item)
    out_file.close()


# Removes Hashtags, URLS, and ReTweets

def removeHashtagsAndURLS(tweet):
    tweet = tweet.split()
    for (i, word) in enumerate(tweet):
        if word.startswith('#') or word.startswith('http') \
            or word.startswith('@'):
            tweet[i] = ''
    return ' '.join(tweet)


# Remove duplicate tweets

def getUniqueTweets(tweets, type_message):
    unique_tweets = []
    unique_types = []
    for (i, tweet) in enumerate(tweets):
        if not unique_tweets.__contains__(tweet):
            unique_tweets.append(tweet)
            unique_types.append(type_message[i])
    return (unique_tweets, unique_types)


# Creates the Blei Corpus

def createCorpus(
    tweets,
    labels,
    labelOutput,
    tweetOutput,
    ):

    # Creates a set of tweets,labels pertaining to non-duplicate tweets

    (documents, labels_unique) = getUniqueTweets(tweets, labels)

    # Clean the tweets by removing Hashtags, URLS, and stopWords

    documents = [removeHashtagsAndURLS(document) for document in
                 documents]
    stoplist = set(stopwords.words('english'))

    # This part is dependent on input file

    texts = [[word.translate(None, ".:?!$&'|-") for word in
             document.lower().split() if word not in stoplist]
             for document in documents]

    # Removes all tokens that occur only once

    all_tokens = Counter()
    for text in texts:
        for word in text:
            all_tokens[word] += 1
    tokens_once = set(word for word in set(all_tokens)
                      if all_tokens[word] == 1)
    texts = [[word for word in text if word not in tokens_once]
             for text in texts]

    # # Remove tweets that are empty after being cleaned

    for (i, listt) in enumerate(texts):
        if len(listt) == 0:
            del texts[i]
            del labels_unique[i]

    # Create a gensim corpus of tweets

    dictionary = corpora.Dictionary(texts)

    # Creates a mapping from token ids to the actual token

    token2id = dictionary.token2id
    id2token = dict((v, k) for (k, v) in token2id.iteritems())
    labels_unique = [(1 if label else -1) for label in labels_unique]
    writeListToFile(labels_unique, labelOutput)

    # Creates the blei-Corpus

    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.BleiCorpus.serialize(tweetOutput, corpus, id2word=id2token)
