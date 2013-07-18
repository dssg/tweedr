import sys
from tweedr.models import DBSession, Tweet, TokenizedLabel, Label

print >> sys.stderr, 'Tweet count started.'
print 'There are %d labels in the database.' % DBSession.query(Label).count()
print 'There are %d tokenized labels in the database.' % DBSession.query(TokenizedLabel).count()

ten_labels = DBSession.query(TokenizedLabel).limit(10).all()

for tokenized_label in ten_labels:
    print repr(tokenized_label)
