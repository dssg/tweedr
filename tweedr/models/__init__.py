import os

from sqlalchemy import create_engine, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
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
    def __unicode__(self):
        type_name = self.__class__.__name__
        pairs = [u'%s=%s' % kv for kv in self.__dict__.items() if kv[0] != '_sa_instance_state']
        return u'<%s %s>' % (type_name, u' '.join(pairs))

    def __repr__(self):
        return unicode(self).encode('utf-8')


Base = declarative_base(metadata=metadata, cls=BaseMixin)


class Label(Base):
    __table__ = Table('labels', metadata, autoload=True)


class TokenizedLabel(Base):
    __table__ = Table('tokenized_labels', metadata, autoload=True)


class Tweet(Base):
    __table__ = Table('tweets', metadata, autoload=True)
