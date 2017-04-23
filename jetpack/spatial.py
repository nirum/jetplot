from scipy.spatial import Delaunay, cKDTree

def in_convex_hull(p, q):
    """
    Test if points in `p` are in convex hull of `q`

    Parameters
    ----------
    p : array_like
        (N x K) array, each row a K-dimensional point to test.

    q : array_like
        (M x K) array, a cloud of K-dimensional points whose convex hull is computed.

    Returns
    -------
    in_hull : ndarray of bools
        N-dimensional vector specifying whether each point in p is in the convex hull of q

    Notes
    -----
    Converted from StackOverflow question: "What's an efficient way to find if a point
    lies in the convex hull of a point cloud?" 
    """
    return Delaunay(q).find_simplex(p)>=0

def nearest_neighbor(p, q, **kwargs):
    """
    Return index into `q` of nearest neighbor for each point in `p`

    Parameters
    ----------
    p : array_like
        (N x K) array, each row a K-dimensional point to query.

    q : array_like
        (M x K) array, a cloud of K-dimensional points references.

    Returns
    -------
    dist :
        N-dimensional vector specifying indices of nearest neighbors.
    idx : ndarray of ints
        N-dimensional vector specifying indices of nearest neighbors.
    """
    return cKDTree(q).query(p, **kwargs)
