import os
import unittest
import pep8


class TestFormatting(unittest.TestCase):
    def test_pep8(self):
        basepath = os.getcwd()
        print 'Running PEP-8 checks on path', basepath
        pep8style = pep8.StyleGuide(paths=[basepath], ignore=['E128', 'E501'])
        report = pep8style.check_files()
        if report.total_errors:
            print report.total_errors

        self.assertEqual(report.total_errors, 0, 'Codebase does not pass PEP-8')
