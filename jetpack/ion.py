"""
IO utilities
"""

import numpy as np

__all__ = ['csv']


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
