import os
import sys

from sqlalchemy import create_engine, MetaData

connection_string = 'mysql+mysqldb://%(MYSQL_USER)s:%(MYSQL_PASS)s@%(MYSQL_HOST)s/%(MYSQL_DATABASE)s' % os.environ
engine = create_engine(connection_string, encoding='latin1', convert_unicode=True)
# yep, it's latin1. Check it:
# mysql -h host-stuff-here.rds.amazonaws.com -u ourusername -p
# SHOW DATABASES;
# USE THEDATABASEWITHSTUFFINIT;
# SHOW VARIABLES LIKE "character_set_database";
metadata = MetaData(bind=engine)


def reflect():
    if sys.stdout.isatty():
        print >> sys.stderr, 'Printing schema to standard output, though you probably want to pipe it into schema.py'
        print >> sys.stderr
        print >> sys.stderr, '    python %s > schema.py' % sys.argv[0]
        print >> sys.stderr

    import mako.template
    template = mako.template.Template(filename='schema.template')
    metadata.reflect()
    sys.stdout.write(template.render(metadata=metadata))

    if not sys.stdout.isatty():
        print >> sys.stderr, 'Done printing schema'

if __name__ == '__main__':
    reflect()
