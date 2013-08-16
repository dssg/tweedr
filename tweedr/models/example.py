import sys
from tweedr.lib.text import whitespace_unicode_translations
from tweedr.models import DBSession, TokenizedLabel, Label

import logging
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)


def count():
    print >> sys.stderr, 'Tweet count started.'
    print 'There are %d labels in the database.' % DBSession.query(Label).count()
    print 'There are %d tokenized labels in the database.' % DBSession.query(TokenizedLabel).count()


def first(limit):
    print >> sys.stderr, 'First %d tweets.' % limit
    for tokenized_label in DBSession.query(TokenizedLabel).limit(limit):
        # print repr(tokenized_label)
        tokenized_label_text = unicode(tokenized_label).translate(whitespace_unicode_translations).encode('utf8')
        token_type_object = tokenized_label.token_type_object
        print token_type_object.id, '\t', token_type_object.text, '\t', tokenized_label_text

first(1000)

# py example.py | awk -F\\t '{print $1,$2}' | sort | uniq -c | sort -g
