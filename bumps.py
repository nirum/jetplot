"""
a raised cosine basis (Keat 2001, Pillow 2005 / 2008)
author: Niru Maheswaranathan
09:51 PM Feb 17, 2014
"""
import numpy as np
from scipy.linalg import orth

def makeRcosBasis(tau, numBases, bias=0.2):
    """
    Makes a raised cosine bases (useful for temporal filters)

    input
    -----
    tau         the time vector along which the bases are generated
    numBases    the number of bases to generate. should be smaller than the length of tau
    bias        a parameter that can make the time scaling more linear (as bias => Inf) or more skewed (as bias => 0) [default is 0.2]

    output
    ------
    Phi         the generated basis vectors
    PhiOrth     the same basis vectors, but orthogonalized

    """

    # bias must be nonnegative
    if bias <= 0:
        raise ValueError('Bias term must be positive.')

    # log-scaled time range to place peak centers, plus a factor for stability
    logTime = np.log(tau + bias + 1e-20);

    # centers for basis vectors
    centers = np.linspace(logTime[0], logTime[-1], numBases);

    # make the basis
    Phi = rcos(logTime.reshape(-1,1), centers.reshape(1,-1), np.mean(np.diff(centers)));
    
    # orthogonalize
    PhiOrth = orth(Phi);

    return Phi, PhiOrth

def rcos(x, c, dc):
    """
    The raised cosine function:
    f(x) = 0.5 * cos(u + 1)

    where u is:
    -pi                 if        (x - c)*pi / 2*dc <  -pi
    (x-c)*pi / 2*dc     if -pi <= (x - c)*pi / 2*dc <= -pi
     pi                 if        (x - c)*pi / 2*dc >   pi

    """

    return 0.5*(np.cos(np.maximum(-np.pi,np.minimum(np.pi,0.5*(x-c)*np.pi/dc)))+1)
