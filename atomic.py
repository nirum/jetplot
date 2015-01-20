"""
Atomic: a set of useful python utilities that don't fit anywhere else
author: Niru Maheswaranathan
04:11 PM Mar 24, 2014
"""
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
from progressbar import ProgressBar

def nrm(x):
    """
    Mean subtract (center) and normalize a set of filters. If a matrix is given, each column is centered and normalized.
    """

    y = x - np.mean(x, axis=0)
    return y / np.linalg.norm(y, axis=0)

def smooth(x,sigma):
    """
    smooths a 1D signal

    smooth(x,sigma)
    """
    return gaussian_filter1d(x,sigma,axis=0)

def sfthr(x,thr):
    """
    soft thresholding function

    sfthr(x,thr)
    """
    return np.sign(x)*np.maximum(np.abs(x)-thr,0)

def dprime(mu1,mu2,var1,var2):
    """
    return the d' metric:

    d' = mu1-mu2 / sqrt(0.5* (var1 + var2))
    """
    return (mu1-mu2) / np.sqrt(0.5*(var1+var2))

def sq(x):
    """
    reshape vector to a square image
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
        rho     = params['rho'] if 'rho' in params else 1           # ADMM momentum term
        lmbda   = params['lambda'] if 'lambda' in params else 0.2   # sparsity penalty
        numiter = params['numiter'] if 'numiter' in params else 100 # number of ADMM iterations
        tol     = params['tol'] if 'tol' in params else 1e-6        # tolerance for convergence

        # initialize
        emp_cov = np.cov(data.T)

        # progress bar
        pb = ProgressBar(numiter)

        # run ADMM
        for itr in range(numiter):

            # update
            pb.animate(itr+1)

            if itr > 0:
                # X-update
                lambdas, Q = np.linalg.eig(rho * (Z-U))     # eigendecomposition of rho*(Z-U)
                x_diag = np.diag((lambdas + np.sqrt(lambdas**2 + 4*rho)) / 2 * rho)
                X = Q.dot(x_diag.dot(Q.T))

            else:
                # initial value
                X = np.linalg.inv(emp_cov)
                U = np.zeros(X.shape)

            # Z-update
            Z = sfthr(X+U, lmbda / rho)

            # U-update (consensus)
            err = X - Z
            U += err

            # check if tolerance is reached
            if np.linalg.norm(err) < tol:
                print('Reached error of %f after %i iterations.' % (np.linalg.norm(err), itr))
                break

        # return estimate
        return np.linalg.inv(X)

    elif method == 'graphlasso':
        model = GraphLassoCV()
        model.fit(data)
        return model.covariance_

    else:
        print('[Error] Unrecognized method ' + method)
