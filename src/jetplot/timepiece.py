"""Utilities for dealing with time."""

import time
from functools import wraps

import numpy as np
from typing import Any, Callable

__all__ = ["hrtime", "Stopwatch", "profile"]


class Stopwatch:
    def __init__(self, name: str = "") -> None:
        self.name = name
        self.start = time.perf_counter()
        self.absolute_start = time.perf_counter()

    def __str__(self) -> str:
        return "\u231a  Stopwatch for: " + self.name

    @property
    def elapsed(self) -> float:
        current = time.perf_counter()
        elapsed = current - self.start
        self.start = time.perf_counter()
        return elapsed

    def checkpoint(self, name: str = "") -> None:
        print(f"{self.name} {name} took {hrtime(self.elapsed)}".strip())

    def __enter__(self) -> "Stopwatch":
        return self

    def __exit__(self, *_: object) -> None:
        total = hrtime(time.perf_counter() - self.absolute_start)
        print(f"{self.name} Finished! \u2714\nTotal elapsed time: {total}")


def hrtime(t: float) -> str:
    """Converts a time in seconds to a reasonable human readable time.

    Args:
      t: float, Time in seconds.

    Returns:
      time: string, Human readable formatted value of the given time.
    """

    # weeks
    if t >= 7 * 60 * 60 * 24:
        weeks = np.floor(t / (7 * 60 * 60 * 24))
        timestr = f"{weeks:0.0f} weeks, " + hrtime(t % (7 * 60 * 60 * 24))

    # days
    elif t >= 60 * 60 * 24:
        days = np.floor(t / (60 * 60 * 24))
        timestr = f"{days:0.0f} days, " + hrtime(t % (60 * 60 * 24))

    # hours
    elif t >= 60 * 60:
        hours = np.floor(t / (60 * 60))
        timestr = f"{hours:0.0f} hours, " + hrtime(t % (60 * 60))

    # minutes
    elif t >= 60:
        minutes = np.floor(t / 60)
        timestr = f"{minutes:0.0f} min., " + hrtime(t % 60)

    # seconds
    elif (t >= 1) | (t == 0):
        timestr = f"{t:g} s"

    # milliseconds
    elif t >= 1e-3:
        timestr = f"{t * 1e3:g} ms"

    # microseconds
    elif t >= 1e-6:
        timestr = f"{t * 1e6:g} \u03bcs"

    # nanoseconds or smaller
    else:
        timestr = f"{t * 1e9:g} ns"

    return timestr



def profile(func: Callable[..., Any]) -> Callable[..., Any]:
    """Timing (profile) decorator for a function."""
    calls = list()

    @wraps(func)
    def wrapper(*args, **kwargs):
        tstart = time.perf_counter()
        results = func(*args, **kwargs)
        tstop = time.perf_counter()
        calls.append(tstop - tstart)
        return results

    def mean() -> float:
        return float(np.mean(calls))

    def serr() -> float:
        return float(np.std(calls) / np.sqrt(len(calls)))

    def summary() -> None:
        print(f"Runtimes: {hrtime(mean())} \u00b1 {hrtime(serr())}")

    wrapper.__dict__["calls"] = calls
    wrapper.__dict__["mean"] = mean
    wrapper.__dict__["serr"] = serr
    wrapper.__dict__["summary"] = summary

    return wrapper
