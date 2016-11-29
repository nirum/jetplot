"""
Plots
-------

Some standard routines for matplotlib plots

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
        
        #fig, axes = plt.subplots(M, M, **skwargs)
        fig = plt.figure(**fig_kwargs)
        axes = np.empty((M,M), dtype=object)
        
        for i in range(M):
            axes[i,i] = fig.add_subplot(M, M, 1+i*(M+1), **subplots_kwargs)

        for i,j in itr.product(range(M), range(M)):
            if i == j:
                continue
            elif i > 0 and j > 0:
                axes[i,j] = fig.add_subplot(M, M, 1+i*M+j, sharex=axes[j,j], sharey=axes[i,0], **subplots_kwargs)
            elif i == 0 and j > 1:
                axes[i,j] = fig.add_subplot(M, M, 1+i*M+j, sharex=axes[j,j], sharey=axes[0,1], **subplots_kwargs)
            else:
                axes[i,j] = fig.add_subplot(M, M, 1+i*M+j, sharex=axes[j,j], **subplots_kwargs)
    
    sc_kwargs = scatter_kwargs.copy()
    sc_kwargs["edgecolor"] = "none" if not "edgecolor" in sc_kwargs.keys() else sc_kwargs["edgecolor"]
    sc_kwargs["c"] = "k" if not "c" in sc_kwargs.keys() else sc_kwargs["c"]
    sc_kwargs["s"] = 10 if not "s" in sc_kwargs.keys() else sc_kwargs["s"]
    
    for i in range(M):
        for j in range(M):
            # make plot
            if i == j:
                axes[i,i].hist(data[i])
                axes[i,i].set_yticks([])
            else:
                axes[i,j].scatter(data[j], data[i], **sc_kwargs)
            
            # first column
            if (i > 0 and j == 0) or (i == 0 and j == M-1):
                axes[i,j].set_ylabel(labels[i])
                yt = axes[i,j].get_yticks()
                axes[i,j].set_yticks([yt[1], yt[-2]])
                if j == M-1:
                    axes[i,j].yaxis.set_ticks_position("right")
                    axes[i,j].yaxis.set_label_position("right")
            else:
                plt.setp(axes[i,j].get_yticklabels(), visible=False)

            # last row
            if i == M-1:
                axes[i,j].set_xlabel(labels[j])
                xt = axes[i,j].get_xticks()
                axes[i,j].set_xticks([xt[1], xt[-2]])
            else:
                plt.setp(axes[i,j].get_xticklabels(), visible=False)
    
    fig.subplots_adjust(hspace=0.0, wspace=0.0, left=0.08, bottom=0.08, top=0.9, right=0.9 )
    return fig, axes
