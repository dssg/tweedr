import os
import sys
import tweedr
from tweedr.lib import walk

source_endings = ('.py', '.bars', '.js', '.md', '.txt', '.mako', '.yml', '.less', '.json', '.css')


def not_egg(filepath):
    return '.egg' not in filepath


def not_git(filepath):
    return '/.git/' not in filepath


def not_static(filepath):
    return '/static/lib/' not in filepath


def is_source(filepath):
    return filepath.endswith(source_endings)


def is_python(filepath):
    return filepath.endswith('.py')


def test_pep8():
    '''Running PEP-8 checks recursively in %s''' % tweedr.root
    import pep8
    ignore = [
        'E128',  # E128 continuation line under-indented for visual indent
        'E501',  # E501 line too long (?? > 79 characters)
    ]
    total_errors = 0
    pep8style = pep8.StyleGuide(ignore=ignore)
    for filepath in walk(tweedr.root, not_egg, not_git, is_python):
        total_errors += pep8style.check_files([filepath]).total_errors

    assert total_errors == 0, 'Codebase does not pass PEP-8 (%d errors)' % total_errors


def test_pyflakes():
    '''Running pyflakes checks recursively in %s''' % tweedr.root
    from pyflakes import api as pyflakes
    total_errors = 0
    for filepath in walk(tweedr.root, not_egg, not_git, is_python):
        total_errors += pyflakes.checkPath(filepath)

    assert total_errors == 0, 'Codebase does not pass pyflakes (%d errors)' % total_errors


def test_trailing_whitespace():
    '''Running trailing whitespace checks recursively in %s''' % tweedr.root
    total_errors = 0
    for filepath in walk(tweedr.root, not_egg, not_git, not_static, is_source):
        with open(filepath) as fp:
            for line_i, raw in enumerate(fp):
                line = raw.rstrip('\n')
                if line.endswith((' ', '\t')):
                    print >> sys.stdout, '%s:%d: trailing whitespace' % (filepath, line_i + 1)
                    total_errors += 1

    assert total_errors == 0, 'Codebase has trailing whitespace (%d errors)' % total_errors


def test_mysql_credentials_no_ci():
    names = ['MYSQL_PASS', 'MYSQL_HOST']
    values = [os.environ[name] for name in names]

    for filepath in walk(tweedr.root):
        with open(filepath) as fp:
            contents = fp.read()
            for value in values:
                assert value not in contents, 'Found a blacklisted credential (%s) in %s' % (value, filepath)
