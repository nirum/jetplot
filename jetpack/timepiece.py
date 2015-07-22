"""
Timepiece: tools for dealing with time
"""

import numpy as np
import time
from functools import wraps

# exports
__all__ = ['hrtime', 'stopwatch']


def stopwatch(fun):
    """Profiling the runtime of a function"""

    @wraps(fun)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = fun(*args, **kwargs)
        end = time.time()
        print('[Stopwatch] %s: %s' % (fun.__name__, hrtime(end-start)))

    return wrapper


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
