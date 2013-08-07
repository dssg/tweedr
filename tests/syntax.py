import sys
import unittest

import pep8
from pyflakes import api as pyflakes

import tweedr
from tweedr.lib import walk

pep8_ignore = [
    'E128',  # E128 continuation line under-indented for visual indent
    'E501',  # E501 line too long (?? > 79 characters)
]


class TestFormatting(unittest.TestCase):
    def test_pep8(self):
        '''Running PEP-8 checks recursively in %s''' % tweedr.root
        pep8style = pep8.StyleGuide(paths=[tweedr.root], ignore=pep8_ignore)
        total_errors = pep8style.check_files().total_errors

        self.assertEqual(total_errors, 0, 'Codebase does not pass PEP-8 (%d errors)' % total_errors)

    def test_pyflakes(self):
        '''Running pyflakes checks recursively in %s''' % tweedr.root
        total_errors = 0
        py_check = lambda s: '.egg' not in s and '/.git/' not in s and s.endswith('.py')
        for filepath in walk(tweedr.root, py_check):
            total_errors += pyflakes.checkPath(filepath)

        self.assertEqual(total_errors, 0, 'Codebase does not pass pyflakes (%d errors)' % total_errors)

    def test_trailing_whitespace(self):
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

        self.assertEqual(total_errors, 0, 'Codebase has trailing whitespace (%d errors)' % total_errors)
