import os


def test_mysql_python_import_no_ci():
    import MySQLdb
    assert MySQLdb is not None, 'MySQLdb should not be None.'


def test_mysql_python_no_ci():
    import MySQLdb
    connection = MySQLdb.connect(
        os.environ['MYSQL_HOST'],
        os.environ['MYSQL_USER'],
        os.environ['MYSQL_PASS'],
        os.environ['MYSQL_DATABASE'])
    cursor = connection.cursor()

    # test version
    version_query = 'SELECT VERSION()'
    cursor.execute(version_query)
    version_result = cursor.fetchone()[0]
    assert version_result.split('.')[0] == '5', 'MySQL major version must equal 5'

    # test schema
    tables_query = 'SELECT TABLE_NAME FROM information_schema.TABLES WHERE TABLE_SCHEMA = "QCRI"'
    cursor.execute(tables_query)
    tables_result = [result[0] for result in cursor.fetchall()]
    table_names = ['tokenized_labels', 'tweets']
    for table_name in table_names:
        assert table_name in tables_result, 'The table "%s" was not found in the database' % table_name

    connection.close()


def test_sqlalchemy_no_ci():
    from sqlalchemy import create_engine, MetaData

    connection_string = 'mysql+mysqldb://%(MYSQL_USER)s:%(MYSQL_PASS)s@%(MYSQL_HOST)s/%(MYSQL_DATABASE)s' % os.environ
    engine = create_engine(connection_string, convert_unicode=True)

    metadata = MetaData(bind=engine)
    metadata.reflect()

    table_names = ['DamageClassification', 'labels']
    for table_name in table_names:
        assert table_name in metadata.tables, 'The table "%s" was not found in SqlAlchemy reflection results' % table_name


def test_tweedr_models_no_ci():
    from tweedr.models import DBSession, TokenizedLabel, Label

    Tables = [TokenizedLabel, Label]
    for Table in Tables:
        row_count = DBSession.query(Table).count()
        assert row_count > 0, 'There should be more than 0 rows in the table "%s"' % Table.name
