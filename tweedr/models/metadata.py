import os

from sqlalchemy import create_engine, MetaData

connection_string = 'mysql+mysqldb://%(MYSQL_USER)s:%(MYSQL_PASS)s@%(MYSQL_HOST)s/%(MYSQL_DATABASE)s' % os.environ
engine = create_engine(connection_string, encoding='latin1', convert_unicode=True)
# yep, it's latin1. Check it:
# mysql -h host-stuff-here.rds.amazonaws.com -u ourusername -p
# SHOW DATABASES;
# USE THEDATABASEWITHSTUFFINIT;
# SHOW VARIABLES LIKE "character_set_database";
metadata = MetaData(bind=engine)
