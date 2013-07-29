import os
import unittest

import tweedr


class TestCredentials(unittest.TestCase):
    def test_mysql(self):
        '''For obvious reasons, Travis CI cannot run this test. Simply pad out
        the test with dummy values when the variables aren't available.'''
        names = ['MYSQL_PASS', 'MYSQL_HOST']
        values = [os.environ.get(name, 'MYSQL_DUMMY_CREDENTIAL') for name in names]

        for base, directories, filenames in os.walk(tweedr.root):
            for filename in filenames:
                filepath = os.path.join(base, filename)
                with open(filepath) as fp:
                    contents = fp.read()
                    for value in values:
                        # assertNotIn(first, second, msg=None)
                        #   Test that first is (or is not) in second.
                        self.assertNotIn(value, contents, 'Found a blacklisted credential (%s) in %s' % (value, filepath))
