## Tests

Most tests use Python's built-in `unittest` test framework.

The `unittest`-powered modules are run by setuptools. At the command line, go to this project's base directory, and run:

    python setup.py test

Alternatively, adding the following snippet to any `tests/*.py` file will let you execute its tests at the command line.

```python
if __name__ == '__main__':
    unittest.main()
```

## `unittest` cheat sheet

From the [documentation](http://docs.python.org/2/library/unittest.html):

> The TestCase class provides a number of methods to check for and report failures, such as:

| Method | Checks that |
|:-------|:------------|
| assertEqual(a, b) | a == b |
| assertNotEqual(a, b) | a != b |
| assertTrue(x) | bool(x) is True |
| assertFalse(x) | bool(x) is False |
| assertIs(a, b) | a is b |
| assertIsNot(a, b) | a is not b |
| assertIsNone(x) | x is None |
| assertIsNotNone(x) | x is not None |
| assertIn(a, b) | a in b |
| assertNotIn(a, b) | a not in b |
| assertIsInstance(a, b) | isinstance(a, b) |
| assertNotIsInstance(a, b) | not isinstance(a, b) |

Each of these methods accepts a final keyword argument, `msg`, which is a string that will be printed if the test does not pass.
