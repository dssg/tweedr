## Tests

Tweedr uses [nose](http://nose.readthedocs.org/) as the test runner.

Tests can be disabled on Travis CI by putting "no_ci" into the test name.

There are three ways to run tests (assuming you have `nose` installed), all of which must be called from the package root directory.

1. `nosetests`
2. `python setup.py test`
3. `python setup.py nosetests`

Travis CI uses the last of these because it's the only one that automatically installs packages from `tests_require` in setup.py as well as allows setting command line options (it uses `-e no_ci` to exclude tests with "no_ci" in their name).
