"""
Heads up display
----------------

"""
import os
import threading
import tempfile
import matplotlib.pyplot as plt
from shutil import rmtree
from functools import wraps
from time import strftime

VALID_FUNCTIONS = {'plot', 'imshow', 'contour', 'contourf', 'semilogx',
                   'semilogy', 'loglog', 'hist', 'hist2d', 'bar', 'pcolor',
                   'pcolormesh', 'scatter', 'fill', 'fill_between', 'errorbar'}
__all__ = ['HUD']


class HUD:

    def __init__(self):
        """
        Starts a HUD server for displaying remote graphics

        Usage:
            >>> hud = HUD()
            >>> hud.plot(my_data)
            >>> hud.imshow(my_image)

        Then, point your browser to `http://localhost:8000` to view the graphics

        """

        plt.switch_backend('agg')

        # Generate a temporary directory
        self.path = tempfile.mkdtemp(prefix='hud_')

        # start the server
        self.start(port=8080)

    def start(self, port):
        self.server = Server(self.path, port=port)
        self.server.start()

    def _plot_wrapper(self, func):

        @wraps(func)
        def wrapper(*args, **kwargs):
            plt.figure()
            plt.ioff()
            func(*args, **kwargs)
            plt.draw()
            filename = os.path.join(self.path, strftime('%b %d %Y %H_%M_%S.jpg'))
            plt.savefig(filename, bbox_inches='tight')
            plt.close()

        return wrapper

    def __iter__(self):
        return iter(os.listdir(self.path))

    def __dir__(self):
        """
        for autocompletion
        """
        return VALID_FUNCTIONS

    def __del__(self):
        rmtree(self.path)

    def __getattr__(self, func):

        if func not in VALID_FUNCTIONS:
            raise ValueError('Function "' + func + '" is not a valid function')

        return self._plot_wrapper(getattr(plt, func))

class Server(threading.Thread):

    def __init__(self, path, port=8000):
        self.path = path
        self.port = port
        super().__init__()

    def run(self):
        """
        Hack to get python to serve the given directory

        """
        cmd = 'cd {}; python3 -m http.server {}'.format(self.path, self.port)
        os.system(cmd)
