import os
import unittest
import pep8
from flake8.main import check_file

import tweedr

pep8_ignore = [
    'E128',  # E128 continuation line under-indented for visual indent
    'E501',  # E501 line too long (?? > 79 characters)
]


class TestFormatting(unittest.TestCase):
    def test_pep8(self):
        print 'Running PEP-8 checks recursively in %s' % tweedr.root
        pep8style = pep8.StyleGuide(paths=[tweedr.root], ignore=pep8_ignore)
        report = pep8style.check_files()

        self.assertEqual(report.total_errors, 0, 'Codebase does not pass PEP-8 (%d errors)' % report.total_errors)

    def test_pyflakes(self):
        print 'Running flake8 on **/*.py in %s' % tweedr.root
        total_errors = 0
        for base, directories, filenames in os.walk(tweedr.root):
            for filename in filenames:
                if filename.endswith('py'):
                    filepath = os.path.join(base, filename)
                    total_errors += check_file(filepath, ignore=pep8_ignore)

        self.assertEqual(total_errors, 0, 'Codebase does not pass flake8 (%d errors)' % total_errors)
