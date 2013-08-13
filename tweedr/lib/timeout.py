'''This module is mostly from github.com/chbrown/remoting
See that repository's readme and /remoting/timeout.py

This is basically how timeouts in Python work:

Use `signal.signal` to queue up a function to run after a specified amount of
time. This function's sole purpose is to raise an exception.

You run your target method, the `func` arg to this decorate() method.
    Two things can happen from here:
    a. Your function finishes before the timeout period. In that case, immediately tell `signal.signal` "just kidding, dont run that function after all." We cancel the scheduled signal from step 1, and put the old handler back in place.
    b. Your function does not finish in time, TimeoutError is raised, and you have to catch it somewhere upstream.

'''
import signal


class TimeoutError(Exception):
    def __call__(self, signum, frame):
        self.args
        raise self

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, self.message)


def timeout_after(seconds):
    '''Closures in python are so beautiful.'''
    def decorate(func):
        def wrapper(*args, **kw):
            new_ALRM = TimeoutError('Timed out after %d seconds.' % seconds)
            old_ALRM = signal.signal(signal.SIGALRM, new_ALRM)
            signal.alarm(seconds)
            try:
                result = func(*args, **kw)
            # we don't handle the error here
            finally:
                # but we do put the old handler back in place
                signal.signal(signal.SIGALRM, old_ALRM)
            signal.alarm(0)
            return result
        wrapper.func_name = func.__name__
        return wrapper
    return decorate


def example():
    '''Usage example. Should be doctests?'''
    import os

    @timeout_after(5)
    def waiter_task(seconds):
        os.system('sleep %d' % seconds)
        return 'Waited %ds successfully' % seconds

    print waiter_task(2)  # --> prints 'Waited 2s successfully'
    print waiter_task(7)  # --> throws


if __name__ == '__main__':
    print example()
