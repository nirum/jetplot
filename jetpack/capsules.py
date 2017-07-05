# -*- coding: utf-8 -*-
"""
Capsules
--------

Custom containers for data

"""
from __future__ import (absolute_import, division, print_function, unicode_literals)
from difflib import get_close_matches
from collections import MutableMapping
from functools import partial

__all__ = ['FuzzyDict', 'pipe']


class FuzzyDict(MutableMapping):
    """
    A fuzzy dictionary (robust wrt spelling errors)

    Lookups are compared to existing keys, if the new key is close enough
    to an existing entry, that entry is recalled
    """
    def __init__(self, threshold=0.6, *args, **kwargs):
        """
        Parameters
        ----------
        threshold : float, optional
            A number between 0 and 1 (default: 0.6). Higher values indicate
            more stringent matching behavior (fewer matches)

        """
        self.store = dict()
        self.threshold = threshold
        self.update(dict(*args, **kwargs))

    def lookup(self, key):
        matches = get_close_matches(key, self.store.keys(), n=1,
                                    cutoff=self.threshold)

        if not matches:
            raise KeyError('Match not found for ' + key)

        return matches[0]

    def __getitem__(self, key):
        return self.store[self.lookup(key)]

    def __setitem__(self, key, value):
        try:
            self.store[self.lookup(key)] = value
        except KeyError:
            self.store[key] = value

    def __delitem__(self, key):
        del self.store[self.lookup(key)]

    def __iter__(self):
        return iter(self.store)

    def __len__(self):
        return len(self.store)


class pipe:
    """
    A wrapper class for pipeline processing

    Usage
    -----
    >> x = np.random.randn(100)
    >> pipe(x) | (smooth, sigma=2.0) | plot
    """
    def __init__(self, payload):
        self.payload = payload

    def __or__(self, other):

        # function and arguments
        if type(other) is tuple:

            assert callable(other[0]), "First argument of the tuple must be callable"
            args = []
            kwargs = []

            if len(other) == 2:
                if type(other[1]) is dict:
                    kwargs = other[1]

                elif type(other[1]) is list:
                    args == other[1]

                else:
                    raise ValueError("Could not parse arguments " + str(other[1]))

            elif len(other) == 3:
                args = other[1]
                kwargs = other[2]

            else:
                args = other[1:]

            fun = partial(other[0], *args, **kwargs)

        # just a function
        elif callable(other):
            fun = other

        else:
            raise ValueError("Not callable: " + str(other))

        return pipe(fun(self.payload))
