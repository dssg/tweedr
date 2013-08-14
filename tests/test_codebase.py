import os
import sys


import tweedr
from tweedr.lib import walk


def test_pep8():
    '''Running PEP-8 checks recursively in %s''' % tweedr.root
    import pep8
    ignore = [
        'E128',  # E128 continuation line under-indented for visual indent
        'E501',  # E501 line too long (?? > 79 characters)
    ]
    pep8style = pep8.StyleGuide(paths=[tweedr.root], ignore=ignore)
    total_errors = pep8style.check_files().total_errors

    assert total_errors == 0, 'Codebase does not pass PEP-8 (%d errors)' % total_errors


def test_pyflakes():
    '''Running pyflakes checks recursively in %s''' % tweedr.root
    from pyflakes import api as pyflakes
    total_errors = 0
    py_check = lambda s: '.egg' not in s and '/.git/' not in s and s.endswith('.py')
    for filepath in walk(tweedr.root, py_check):
        total_errors += pyflakes.checkPath(filepath)

    assert total_errors == 0, 'Codebase does not pass pyflakes (%d errors)' % total_errors


def test_trailing_whitespace():
    '''Running trailing whitespace checks recursively in %s''' % tweedr.root
    total_errors = 0
    source_endings = ('.py', '.bars', '.js', '.md', '.txt', '.mako', '.yml', '.less', '.json', '.css')
    source_check = lambda s: '/static/lib/' not in s and '/.git/' not in s and s.endswith(source_endings)
    for filepath in walk(tweedr.root, source_check):
        with open(filepath) as fp:
            for line_i, raw in enumerate(fp):
                line = raw.rstrip('\n')
                if line.endswith((' ', '\t')):
                    print >> sys.stderr, '%s:%d: trailing whitespace' % (filepath, line_i + 1)
                    total_errors += 1

    assert total_errors == 0, 'Codebase has trailing whitespace (%d errors)' % total_errors


def test_mysql_credentials_no_ci():
    names = ['MYSQL_PASS', 'MYSQL_HOST']
    values = [os.environ[name] for name in names]

    for base, directories, filenames in os.walk(tweedr.root):
        for filename in filenames:
            filepath = os.path.join(base, filename)
            with open(filepath) as fp:
                contents = fp.read()
                for value in values:
                    # assertNotIn(first, second, msg=None)
                    #   Test that first is (or is not) in second.
                    assert value not in contents, 'Found a blacklisted credential (%s) in %s' % (value, filepath)
