"""
Utils: common ipython / python utilities

"""

# imports
import numpy as np
import time
from functools import wraps
from contextlib import contextmanager

# exports
__all__ = ['profile', 'hrtime', 'stopwatch']


@contextmanager
def stopwatch(label):
    start = time.time()

    try:
        yield

    finally:
        end = time.time()
        print('[Stopwatch] %s: %s' % (label, hrtime(end-start)))


def profile(f):
    """
    Function decorator for profiling a function

    Measures the runtime of the given function

    Parameters
    ----------
    f : function
        The function to be profiled

    """
    @wraps(f)
    def profile_wrapper(*args, **kwds):
        start = time.time()
        res = f(*args, **kwds)
        print("Runtime: " + hrtime(time.time() - start))

        return res

    return profile_wrapper


def hrtime(t):
    """
    Converts a time in seconds to a reasonable human readable time

    Parameters
    ----------
    t : float
        The number of seconds

    Returns
    -------
    time : string
        The human readable formatted value of the given time

    """

    # days
    if t >= 60*60*24:
        days = np.floor(t / (60.*60.*24.))
        timestr = ("%i days, " % days) + hrtime(t % (60*60*24))

    # hours
    elif t >= 60*60:
        hours = np.floor(t / (60.*60.))
        timestr = ("%i hours, " % hours) + hrtime(t % (60*60))

    # minutes
    elif t >= 60:
        minutes = np.floor(t / 60.)
        timestr = ("%i minutes, " % minutes) + hrtime(t % 60)

    # seconds
    elif (t >= 1) | (t == 0):
        timestr = "%0.0f seconds" % t

    # milliseconds
    elif t >= 1e-3:
        timestr = "%0.0f milliseconds" % (t*1e3)

    # microseconds
    else:
        timestr = "%0.0f microseconds" % (t*1e6)

    return timestr
