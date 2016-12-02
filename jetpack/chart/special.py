"""
Special
-------

Some canned routines for making specialized plots in matplotlib

"""

import numpy as np
import matplotlib.pyplot as plt
import itertools as itr

def plotmatrix(data, labels=None, axes=None, subplots_kwargs=dict(),
               scatter_kwargs=dict(), **fig_kwargs):
    """ Create a scatter plot matrix from the given data. 
        
        Note
        ----
        This code was modified from: https://gist.github.com/adrn/5301190

        Parameters
        ----------
        data : numpy.ndarray
            A numpy array containined the scatter data to plot. The data
            should be shape MxN where M is the number of dimensions and 
            with N data points.
        labels : numpy.ndarray (optional)
            A numpy array of length M containing the axis labels.
        axes : matplotlib Axes array (optional)
            If you've already created the axes objects, pass this in to
            plot the data on that.
        subplots_kwargs : dict (optional)
            A dictionary of keyword arguments to pass to the 
            matplotlib.pyplot.subplots call. Note: only relevant if axes=None.
        scatter_kwargs : dict (optional)
            A dictionary of keyword arguments to pass to the 
            matplotlib.pyplot.scatter function calls.
        **fig_kwargs
            Additional keyword arguments are passed to the
            matplotlib.pyplot.figure call.
    """
        
    try:
        M,N = data.shape
        if M > N: raise ValueError()
    except ValueError: # too many values to unpack
        raise ValueError("Invalid data shape {0}. You must pass in an array of "
                         "shape (M, N) where N > M.".format(data.shape))
    
    if labels == None:
        labels = ['']*M
    
    if axes == None:
        skwargs = subplots_kwargs.copy()
        
    fig, axes = plt.subplots(M, M, **subplots_kwargs)
    
    sc_kwargs = scatter_kwargs.copy()
    sc_kwargs["edgecolor"] = "none" if not "edgecolor" in sc_kwargs.keys() else sc_kwargs["edgecolor"]
    sc_kwargs["c"] = "k" if not "c" in sc_kwargs.keys() else sc_kwargs["c"]
    sc_kwargs["s"] = 10 if not "s" in sc_kwargs.keys() else sc_kwargs["s"]
    
    # Axes properties
    xmin = np.empty((M,M))
    xmax = np.empty((M,M))
    ymin = np.empty((M,M))
    ymax = np.empty((M,M))

    # First, go through and make plots
    for i in range(M):
        for j in range(M):
            # make plot
            if i == j:
                axes[i,i].hist(data[i])
                axes[i,i].set_yticks([])
            else:
                axes[i,j].scatter(data[j], data[i], **sc_kwargs)

            xmin[i,j], xmax[i,j] = axes[i,j].get_xlim()
            
            # ignore y-axes on histograms
            if i == j:
                ymin[i,j], ymax[i,j] = np.nan(), np.nan()
            else:
                ymin[i,j], ymax[i,j] = axes[i,j].get_ylim()
    
    # get axes limits for each row/col
    x0_ = np.min(xmin, axis=0)
    x1_ = np.max(xmax, axis=0)
    y0_ = np.nanmin(ymin, axis=1)
    y1_ = np.nanmax(ymax, axis=1)

    # Make a second pass over the plots to format axes
    for i, y0 in enumerate(y0_):
        for j, x0 in enumerate(x0_):

            # set axis limits
            axes[i,j].set_xlim([x0, x1])
            axes[i,j].set_ylim([y0, y1])

            # set spine color
            for spine in ax.spines.values():
                spine.set_color('gray')

            # format left-most column
            if (i > 0 and j == 0) or (i == 0 and j == M-1):
                axes[i,j].set_ylabel(labels[i])
                yt = axes[i,j].get_yticks()
                axes[i,j].set_yticks([yt[1], yt[-2]])
                
                # the top row is a special case
                if j == M-1:
                    axes[i,j].yaxis.set_ticks_position("right")
                    axes[i,j].yaxis.set_label_position("right")
            else:
                plt.yticks([])

            # last row
            if i == M-1:
                axes[i,j].set_xlabel(labels[j])
                xt = axes[i,j].get_xticks()
                axes[i,j].set_xticks([xt[1], xt[-2]])
            else:
                plt.setp(axes[i,j].get_xticklabels(), visible=False)

    fig.subplots_adjust(hspace=0.0, wspace=0.0, left=0.08, bottom=0.08, top=0.9, right=0.9 )
    return fig, axes
