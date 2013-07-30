import os
import unittest

import tweedr


class TestCredentials(unittest.TestCase):
    def test_mysql(self):
        if 'TRAVIS' in os.environ:
            print 'For obvious reasons, Travis CI cannot run this test.'
        else:
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
                            self.assertNotIn(value, contents, 'Found a blacklisted credential (%s) in %s' % (value, filepath))
