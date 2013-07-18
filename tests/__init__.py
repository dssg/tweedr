import os
import subprocess
import unittest


class TestFormatting(unittest.TestCase):
    def test_pep8(self):
        basepath = os.getcwd()
        print 'pep8 starting in', basepath
        returncode = subprocess.call(['pep8', basepath, '--ignore=E128,E501'])
        self.assertEqual(returncode, 0, 'Codebase does not pass PEP-8')
