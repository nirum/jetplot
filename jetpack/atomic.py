"""
Atomic: a set of useful python utilities that don't fit anywhere else
04:11 PM Mar 24, 2014

"""

import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from progressbar import ProgressBar

def norms(x, order=2):
    """
    Normalize a set of filters according to the given norm.
    If a matrix is given, each column is centered and normalized.

    Parameters
    ----------
    x : array_like
        The array (or matrix) to be normalized.

    order : {non-zero int, inf, -inf, 'fro'}, optional
        Order of the norm to use when normalizing the input. Default is 2.

    Returns
    -------
    xn : array_like
        The input array scaled to have unit norm columns.

    Notes
    -----
    For values of ``ord <= 0``, the result is, strictly speaking, not a
    mathematical 'norm', but it may still be useful for various numerical
    purposes.

    The following norms can be calculated:

    =====  ==========================
    ord    norm for vectors
    =====  ==========================
    None   2-norm
    inf    max(abs(x))
    -inf   min(abs(x))
    0      sum(x != 0)
    other  sum(abs(x)**ord)**(1./ord)
    =====  ==========================

    """

    return x / np.linalg.norm(x, axis=0, ord=order)

def smooth(x, sigma):
    """
    Smooths a 1D signal with a gaussian filter

    Parameters
    ----------
    x : array_like
        The array to be smoothed

    sigma : float
        The width of the gaussian filter

    Returns
    -------
    xs : array_like
        A smoothed version of the input signal

    """

    return gaussian_filter1d(x, sigma, axis=0)

def sfthr(x,threshold):
    """
    Soft thresholding function

    Parameters
    ----------
    x : array_like
        The input array to the soft thresholding function

    threshold : float
        The threshold of the function

    Returns
    -------
    y : array_like
        The output of the soft thresholding function

    """

    return np.sign(x) * np.maximum(np.abs(x) - threshold, 0)

def dprime(mu1,mu2,var1,var2):
    """
    Return the d' metric given the mean and variance of two distributions

    d' = mu1-mu2 / sqrt(0.5* (var1 + var2))

    """

    return (mu1 - mu2) / np.sqrt(0.5 * (var1 + var2))

def sq(x):
    """
    Reshape vector to a square image

    """
    return x.reshape(int(np.sqrt(x.size)),-1)

def sice(data, method='admm', params=None):
    """
    sparse inverse covariance estimation
    via sklearn.covariance GraphLassoCV

    input: data (n_samples by n_features)

    returns: Estimated covariance (n_features by n_features)

    """
    from sklearn.covariance import GraphLassoCV

    n_samples, n_features = data.shape
    print('%i samples of a %i dimensional feature space.' % (n_samples, n_features))

    # center / normalize
    data -= data.mean(axis=0)
    data /= data.std(axis=0)

    if method == 'admm':

        if params is None:
            params = dict()

        # parameters / options
        rho     = params['rho'] if 'rho' in params else 1            # ADMM momentum term
        lmbda   = params['lambda'] if 'lambda' in params else 0.2    # sparsity penalty
        numiter = params['numiter'] if 'numiter' in params else 100  # number of ADMM iterations
        tol     = params['tol'] if 'tol' in params else 1e-6         # tolerance for convergence

        # initialize
        emp_cov = np.cov(data.T)

        # progress bar
        pb = ProgressBar(numiter)

        # initial values of variables
        inv_cov_x = np.linalg.inv(emp_cov)
        inv_cov_z = np.zeros_like(inv_cov_x)
        dual_err = np.zeros(inv_cov_x.shape)

        # run ADMM
        for itr in range(numiter):

            # update
            pb.animate(itr + 1)

            if itr > 0:
                # inv_cov_x-update
                lambdas, eigenvectors = np.linalg.eig(rho * (inv_cov_z - dual_err))
                x_diag = np.diag((lambdas + np.sqrt(lambdas ** 2 + 4 * rho)) / 2 * rho)
                inv_cov_x = eigenvectors.dot(x_diag.dot(eigenvectors.T))

            # inv_cov_z-update
            inv_cov_z = sfthr(inv_cov_x + dual_err, lmbda / rho)

            # dual_err-update (consensus)
            err = inv_cov_x - inv_cov_z
            dual_err += err

            # check if tolerance is reached
            if np.linalg.norm(err) < tol:
                print('Reached error of %f after %i iterations.' % (np.linalg.norm(err), itr))
                break

        # return estimate
        return np.linalg.inv(inv_cov_x)

    elif method == 'graphlasso':
        model = GraphLassoCV()
        model.fit(data)
        return model.covariance_

    else:
        print('[Error] Unrecognized method ' + method)
