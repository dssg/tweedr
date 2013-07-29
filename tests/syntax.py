import unittest
import pep8
from pyflakes import api as pyflakes

import tweedr

pep8_ignore = [
    'E128',  # E128 continuation line under-indented for visual indent
    'E501',  # E501 line too long (?? > 79 characters)
    'F401',  # F401 '???' imported but unused
]


class TestFormatting(unittest.TestCase):
    def test_pep8(self):
        print 'Running PEP-8 checks recursively in %s' % tweedr.root
        pep8style = pep8.StyleGuide(paths=[tweedr.root], ignore=pep8_ignore)
        total_errors = pep8style.check_files().total_errors

        self.assertEqual(total_errors, 0, 'Codebase does not pass PEP-8 (%d errors)' % total_errors)

    def test_pyflakes(self):
        print 'Running pyflakes checks recursively in %s' % tweedr.root
        # checkRecursive(paths, reporter) but oddly, reporter does not default to None,
        #   though a None reporter is replaced with the default later down the line
        total_errors = pyflakes.checkRecursive([tweedr.root], None)

        self.assertEqual(total_errors, 0, 'Codebase does not pass pyflakes (%d errors)' % total_errors)
