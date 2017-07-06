"""
Jetpack animation
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from moviepy.editor import VideoClip
from moviepy.video.io.bindings import mplfig_to_npimage

__all__ = ['save_movie', 'play', 'save_frames']


def save_movie(make_frame, duration, filename, fps=20):
    """Writes an animation to disk"""
    anim = VideoClip(make_frame, duration=duration)

    if filename.endswith('.gif'):
        anim.write_gif(filename, fps=fps)

    elif filename.endswith('.mp4'):
        anim.write_videofile(filename, fps=fps)

    else:
        raise ValueError(f'Invalid file type for {filename}. Must be .gif or .mp4')

    return anim


def play(frames, repeat=True, fps=15, cmap='seismic_r', clim=None):
    """Plays the stack of frames as a movie"""
    # Set up the figure
    fig = plt.figure()
    plt.axis('equal')
    ax = plt.axes(xlim=(0, frames.shape[1]), ylim=(0, frames.shape[2]))
    img = plt.imshow(frames[0])
    ax.set_xticks([])
    ax.set_yticks([])

    # Set up the colors
    img.set_cmap(cmap)
    img.set_interpolation('nearest')
    if clim is None:
        maxval = np.max(np.abs(frames))
        img.set_clim([-maxval, maxval])
    else:
        img.set_clim(clim)

    # Animation function (called sequentially)
    def animate(i):
        # ax.set_title('Frame {0:#d}'.format(i + 1))
        img.set_data(frames[i])

    # Call the animator
    dt = 1000 / fps
    anim = animation.FuncAnimation(fig, animate, np.arange(frames.shape[0]),
                                   interval=dt, repeat=repeat)
    plt.show()
    plt.draw()

    return anim


def save_frames(frames, filename, cmap='seismic_r', T=None, clim=None, fps=15, figsize=None):
    """Saves the stack of frames as a movie"""
    fig = plt.figure(figsize=figsize)
    ax = fig.add_subplot(111)

    # total length
    if T is None:
        T = frames.shape[0]

    # mean subtract
    X = frames.copy()
    # X -= X.mean()

    img = ax.imshow(X[0])
    ax.axis('off')
    ax.set_aspect('equal')
    ax.set_xlim(0, X.shape[1])
    ax.set_ylim(0, X.shape[2])
    ax.set_xticks([])
    ax.set_yticks([])

    # Set up the colors
    img.set_cmap(cmap)
    img.set_interpolation('nearest')
    if clim is None:
        maxval = np.max(np.abs(X))
        img.set_clim([-maxval, maxval])
    else:
        img.set_clim(clim)

    plt.show()
    plt.draw()

    dt = 1 / fps

    def animate(t):
        i = np.mod(int(t / dt), T)
        # ax.set_title(f't={i*0.01:2.2f} s')
        img.set_data(X[i])
        return mplfig_to_npimage(fig)

    save_movie(animate, T * dt, filename, fps=fps)
