"""
IO utilities
"""

import numpy as np

__all__ = ['csv']


def csv(filename, data, headers):
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

    """

    if not filename.endswith('.csv'):
        filename += '.csv'

    assert data.shape[1] == len(headers), \
        "The array must have the same number of columns as the headers input"

    np.savetxt(filename + '.csv', data, delimiter=',',
               header=','.join(headers), comments='')
