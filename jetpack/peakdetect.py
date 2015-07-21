import sys
from numpy import NaN, Inf, arange, isscalar, array, asarray

def peakdet(v, delta, x=None):
    """
    Finds local optima (maxima and minima) of a 1D signal.

    Usage
    -----
    maxtab, mintab = peakdet(v, delta=0.5)

    Parameters
    ----------
    v : array_like
        The 1D signal in which we wish to find local optima

    delta : float
        Optima are accepted if they are at least delta greater than neighboring values

    x : array_like, optional
        Used to return the x-values of the optima. If None (default), indices into the `v` array are returned.

    Returns
    -------
    maxtab : array_like
        (N x 2) array, where the first column are the maxima and the second column are the locations of those maxima.

    mintab : array_like
        (N x 2) array, where the first column are the minima and the second column are the locations of those minima.

    Notes
    -----
    Converted from MATLAB script at http://billauer.co.il/peakdet.html

    """

    maxtab = []
    mintab = []

    if x is None:
        x = arange(len(v))

    v = asarray(v)

    if len(v) != len(x):
        sys.exit('Input vectors v and x must have same length')

    if not isscalar(delta):
        sys.exit('Input argument delta must be a scalar')

    if delta <= 0:
        sys.exit('Input argument delta must be positive')

    mn, mx = Inf, -Inf
    mnpos, mxpos = NaN, NaN

    lookformax = True

    for i in arange(len(v)):
        this = v[i]
        if this > mx:
            mx = this
            mxpos = x[i]
        if this < mn:
            mn = this
            mnpos = x[i]

        if lookformax:
            if this < mx-delta:
                maxtab.append((mxpos, mx))
                mn = this
                mnpos = x[i]
                lookformax = False
        else:
            if this > mn+delta:
                mintab.append((mnpos, mn))
                mx = this
                mxpos = x[i]
                lookformax = True

    return array(maxtab), array(mintab)
