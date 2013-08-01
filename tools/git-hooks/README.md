## git hooks

`pre-commit` requires all tests to pass before you commit.

Here's the entire file:

```bash
#!/bin/sh
cd $(dirname $GIT_DIR)
python setup.py test
```

Install:

```bash
cd tweedr
cp tools/git-hooks/pre-commit .git/hooks/pre-commit
```
