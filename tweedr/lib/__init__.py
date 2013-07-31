import os
import sys
import fnmatch
import random
import subprocess
from copy import copy


def stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()


def stderrn(s=''):
    stderr(str(s) + os.linesep)


def stdout(s):
    sys.stdout.write(s)
    sys.stdout.flush()


def stdoutn(s=''):
    stdout(str(s) + os.linesep)


def tty_size():
    height, width = subprocess.check_output(['stty', 'size']).split()
    return (int(height), int(width))


def uniq(xs):
    # order preserving. From http://www.peterbe.com/plog/uniqifiers-benchmark
    seen = {}
    checked = []
    for x in xs:
        if x in seen:
            continue
        seen[x] = 1
        checked.append(x)
    return checked


def iglob(pattern, root='.'):
    for dirpath, dirnames, filenames in os.walk(root):
        filepaths = [os.path.join(dirpath, filename) for filename in filenames]
        for filepath in fnmatch.filter(filepaths, pattern):
            yield filepath


def walk(top, pred=None):
    # if pred is not None, pred(filepath) must be True for each filepath to be returned
    for dirpath, dirnames, filenames in os.walk(top):
        filepaths = [os.path.join(dirpath, filename) for filename in filenames]
        for filepath in filepaths:
            if pred is None or pred(filepath):
                yield filepath


def bifurcate(xs, ratio, shuffle=False):
    '''
    Takes a list like [b, c, a, m, n] and ratio like 0.6 and returns two lists: [b, c, a], [m, n]

    E.g.,

        test, train = bifurcate(tokenized_labels, test_proportion, shuffle=True)
    '''
    length = len(xs)
    pivot = int(ratio * length)
    if shuffle:
        xs = copy(xs)
        random.shuffle(xs)

    return (xs[:pivot], xs[pivot:])


class Counts(object):
    def __init__(self):
        object.__setattr__(self, '_store', {})

    def __getattr__(self, name):
        return self._store.get(name, 0)

    def __setattr__(self, name, value):
        self._store[name] = value

    def empty_copy(self):
        other = Counts()
        other._store = dict((name, 0) for name in self._store)
        return other

    def add(self, other):
        for name, value in other._store.items():
            self._store[name] = self._store.get(name, 0) + value

    def __repr__(self):
        return '<Counts %s>' % ' '.join('%s=%d' % (name, value) for name, value in self._store.items())
