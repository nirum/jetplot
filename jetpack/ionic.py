"""
Ionic
-----

IO and display utilities
"""

import numpy as np
from numbers import Number

__all__ = ['csv', 'as_percent', 'unicodes']


def csv(filename, data, headers, fmt='%g'):
    """
    Write a numpy array to a CSV file with the given headers

    Parameters
    ----------
    filename : string
        The filename of the CSV file to write

    data : array_like
        A numpy array (matrix) containing the data to write

    headers : list
        List of strings corresponding to the column headers

    fmt : string, optional
        A format string for how to encode the data (Default: '%g')

    """

    if not filename.endswith('.csv'):
        filename += '.csv'

    assert data.shape[1] == len(headers), \
        "The array must have the same number of columns as the headers input"

    np.savetxt(filename, data, delimiter=',', fmt=fmt,
               header=','.join(headers), comments='')


def as_percent(x, precision='0.2'):
    """
    Convert number to percentage string.
    """
    if isinstance(x, Number):
        return "{{:{}%}}".format(precision).format(x)
    else:
        raise TypeError("Numeric type required")


unicodes = {
    'mu': u'\u03BC',
    'lambda': u'\u03BB',
    'gamma': u'\u03B3',
    'pi': u'\u03C0',
    'Pi': u'\u220F',
    'tau': u'\u03C4',
    'sigma': u'\u03C3',
    'rho': u'\u03C1',
    'kappa': u'\u03BA',
    'theta': u'\u03B8',
    'epsilon': u'\u03B5',
    'delta': u'\u03B4',
    'Delta': u'\u0394',
    'phi': u'\u03C6',
    'Phi': u'\u03A6',
    'check': u'\u2714',
    'x': u'\u2718',
    'star': u'\u272F',
    'arrow': u'\u279B',
    'gradient': u'\u2206',
    'nabla': u'\u2207',
    'in': u'\u2208',
    'exists': u'\u2203',
    'forall': u'\u2200',
    'not_in': u'\u2209',
    'int': u'\u222B',
    'partial': u'\u2202',
    'sqrt': u'\u221A',
    'geq': u'\u2265',
    'leq': u'\u2264',
    'neq': u'\u2260',
    'approx': u'\u2243',
    'infty': u'\u221E',
    'cdot': u'\u2219',
    'Sigma': u'\u2211',
    'prod': u'\u220F'
}
