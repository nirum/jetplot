"""
Tests for the timepiece module

"""

from jetpack.timepiece import hrtime
from jetpack.ionic import unicodes
import pytest


def test_hrtime():

    # test numeric input
    assert hrtime(1e6) == u'1 weeks, 4 days, 13 hours, 46 min., 40 s'
    assert hrtime(2e5) == u'2 days, 7 hours, 33 min., 20 s'
    assert hrtime(5e3) == u'1 hours, 23 min., 20 s'
    assert hrtime(60) == u'1 min., 0 s'
    assert hrtime(1) == u'1 s'
    assert hrtime(0) == u'0 s'
    assert hrtime(0.1) == u'100 ms'
    assert hrtime(0.005) == u'5 ms'
    assert hrtime(1e-5) == u'10 {}s'.format(unicodes['mu'])
    assert hrtime(5.25e-4) == u'525 {}s'.format(unicodes['mu'])
    assert hrtime(5e-7) == u'500 ns'
    assert hrtime(1e-12) == u'0.001 ns'

    # test non-numeric input
    for val in ('abc', [], {'x': 5}):

        with pytest.raises(ValueError) as context:
            hrtime(val)

        assert 'Input must be numeric' in str(context.value)
