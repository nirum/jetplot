# -*- coding: utf-8 -*-
"""
Visualization tools for animations
"""
from moviepy.video.io.bindings import mplfig_to_npimage
import moviepy.editor as mpy
import matplotlib.pyplot as plt

def movieclip(makeframe, ax=None, **kwargs):

    # grab figure and axes handles
    fig = plt.gcf()
    if ax is None:
        ax = plt.gca()

    # wrap makeframe function with mpltfig_to_npimage
    def _makeframe(t):
        print(t)
        makeframe(int(t), ax=ax)
        return mplfig_to_npimage(plt.gcf())

    # return clip
    return mpy.VideoClip(_makeframe, **kwargs)
