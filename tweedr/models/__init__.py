import os
from tweedr.lib.text import token_re

from sqlalchemy import create_engine, MetaData  # , Table
from sqlalchemy.ext.declarative import declarative_base, DeferredReflection
from sqlalchemy.orm import sessionmaker as sessionmakermaker

connection_string = 'mysql+mysqldb://%(MYSQL_USER)s:%(MYSQL_PASS)s@%(MYSQL_HOST)s/%(MYSQL_DATABASE)s' % os.environ
engine = create_engine(connection_string, encoding='latin1', convert_unicode=True)
# yep, it's latin1. Check it:
# mysql -h host-stuff-here.rds.amazonaws.com -u ourusername -p
# SHOW DATABASES;
# USE THEDATABASEWITHSTUFFINIT;
# SHOW VARIABLES LIKE "character_set_database";
sessionmaker = sessionmakermaker(bind=engine)
DBSession = sessionmaker()
metadata = MetaData(bind=engine)


class BaseMixin(object):
    def __json__(self):
        # this serves to both copy the record's values as well as filter out the special sqlalchemy key
        return dict((k, v) for k, v in self.__dict__.items() if k != '_sa_instance_state')

    def __unicode__(self):
        type_name = self.__class__.__name__
        pairs = [u'%s=%s' % (k, v) for k, v in self.__json__().items()]
        return u'<%s %s>' % (type_name, u' '.join(pairs))

    def __repr__(self):
        return unicode(self).encode('utf-8')


Base = declarative_base(metadata=metadata, cls=BaseMixin)


class Label(DeferredReflection, Base):
    # __table__ = Table('labels', metadata, autoload=True)
    __tablename__ = 'labels'


class TokenizedLabel(DeferredReflection, Base):
    # __table__ = Table('tokenized_labels', metadata, autoload=True)
    __tablename__ = 'tokenized_labels'

    @property
    def tokens(self):
        return token_re.findall(unicode(self.tweet).encode('utf8'))

    @property
    def labels(self):
        labels = []
        label_start, label_end = self.token_start, self.token_end
        for match in token_re.finditer(self.tweet):
            token_start, token_end = match.span()
            # token = match.group(0)
            # we want to determine if this particular token in the original tweet overlaps
            #   with any portion of the selected label (label_span)
            if label_start <= token_start <= label_end or label_start <= token_end <= label_end:
                labels.append(self.token_type)
            else:
                # should I let the user set the NA label?
                labels.append(None)
        return [unicode(label).encode('utf8') for label in labels]


class Tweet(DeferredReflection, Base):
    # __table__ = Table('tweets', metadata, autoload=True)
    __tablename__ = 'tweets'

# DeferredReflection is just as slow as the __table__(autoload=True) calls.
# I thought it might be faster, but not really.
DeferredReflection.prepare(engine)
