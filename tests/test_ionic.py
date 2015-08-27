"""
Tests for the ionic module

"""

from jetpack import ionic
import os
import tempfile
import filecmp
import numpy as np
import pytest


def test_csv():

    # write to csv
    fname = 'test_datafile'
    data = np.arange(5).reshape(1, 5)
    headers = list('abcde')
    ionic.csv(fname, data, headers, fmt="%d")

    # manually create the same file
    tmpfile = tempfile.NamedTemporaryFile(mode='w+', delete=True)
    tmpfile.write('a,b,c,d,e\n0,1,2,3,4\n')
    tmpfile.flush()

    assert filecmp.cmp(fname + '.csv', tmpfile.name)

    # clean up
    tmpfile.close()
    os.remove(fname + '.csv')


def test_as_percent():

    assert ionic.as_percent(0.425) == '42.50%'
    assert ionic.as_percent(0.218, precision='0.1') == '21.8%'
    assert ionic.as_percent(0.02) == '2.00%'
    assert ionic.as_percent(0.91, precision='0.0') == '91%'


def test_as_percent_numeric_value():

    with pytest.raises(TypeError) as context:
        ionic.as_percent(u'0.50')

    assert 'Numeric type required' in str(context.value)
