"""
Capsules
--------

Custom containers for data

"""

from difflib import get_close_matches
from collections import MutableMapping

__all__ = ['FuzzyDict']


class FuzzyDict(MutableMapping):

    def __init__(self, thr=0.6, *args, **kwargs):
        """
        Parameters
        ----------
        thr : float, optional
            A number between 0 and 1 (default: 0.6). Higher values indicate
            more stringent matching behavior (fewer matches)

        """
        self.store = dict()
        self.threshold = thr
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
