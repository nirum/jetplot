"""
Matlab
-----

Tools for interfacing with Matlab

"""

import scipy.io as spio
import numpy as np

def loadmat(filename):
    '''
    this function should be called instead of direct spio.loadmat
    as it cures the problem of not properly recovering python dictionaries
    from mat files. It calls the function check keys to cure all entries
    which are still mat-objects
    '''
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)

    # convert to numpy
    for key in data:
        data[key] = _mat_to_dict(data[key])

    return data

def _mat_to_dict(obj):
    '''
    A recursive function which constructs nested dictionaries from matlab
    structs
    '''

    # if obj is a struct, recursively construct dict
    if isinstance(obj, spio.matlab.mio5_params.mat_struct):
        dest = {}
        for strg in obj._fieldnames:
            elem = obj.__dict__[strg]
            dest[strg] = _mat_to_dict(elem)
        return dest

    # recursive call to convert struct arrays
    elif isinstance(obj, np.ndarray):
        return np.array([_mat_to_dict(elem) for elem in obj])

    # base case
    else:
        return obj
